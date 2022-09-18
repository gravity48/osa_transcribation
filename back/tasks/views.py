import json
from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import generic

from connections.models import Connections
from transcribing_web.celery import app
from . import models, forms, tasks

ACTIVE_STATUS = 1

event_list = {'add_task', 'del_task', 'play', 'stop'}


def parse_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_map = {'error': 'No event', }
        try:
            data = json.loads(args[0].body)
            event = data['event']
        except (ValueError, json.JSONDecodeError):
            return JsonResponse(error_map, status=settings.DEFAULT_ERROR_STATUS)
        if event in event_list:
            kwargs['event'] = event
            kwargs['data'] = data
            response = func(*args, **kwargs)
            return response
        else:
            return JsonResponse(error_map, status=settings.DEFAULT_ERROR_STATUS)

    return wrapper


post_decorators = [login_required, parse_event]


@method_decorator(post_decorators, name='post')
class TasksView(generic.View):
    template_name = 'tasks/tasks.html'

    @staticmethod
    def _add_task(data):
        tasks_form = forms.TasksForm(data)
        if tasks_form.is_valid():
            language = models.LanguageList.objects.get(pk=tasks_form.cleaned_data['language_id'])
            connection = models.Connections.objects.get(pk=tasks_form.cleaned_data['connection_id'])
            models.Tasks(db=connection, language=language, alias=tasks_form.cleaned_data['alias'],
                         period_from=tasks_form.cleaned_data['period_from'],
                         period_to=tasks_form.cleaned_data['period_to'], log=tasks_form.cleaned_data['log'],
                         thread_count=tasks_form.cleaned_data['thread_count'],
                         time_processing=tasks_form.cleaned_data['time_processing']).save()
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            errors = json.loads(tasks_form.errors.as_json())
            return errors, settings.DEFAULT_ERROR_STATUS

    @staticmethod
    def _del_task(data):
        del_task_form = forms.DelTaskForm(data)
        if del_task_form.is_valid():
            task_id = del_task_form.cleaned_data['task_id']
            models.Tasks.objects.get(pk=task_id).delete()
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            errors = json.loads(del_task_form.errors.as_json())
            return errors, settings.DEFAULT_ERROR_STATUS

    def _play_task(self, data):
        try:
            task_id = int(data['task_id'])
            task = models.Tasks.objects.get(pk=task_id)
        except (KeyError, models.Tasks.DoesNotExist):
            return {'error': 'No task'}, settings.DEFAULT_ERROR_STATUS
        task_params = models.Tasks.objects.values('id', 'db__ip', 'db__port', 'db__db_name', 'db__db_login',
                                                  'db__db_password',
                                                  'db__db_system__name', 'period_from', 'period_to', 'language__model',
                                                  'language__short_name', 'log', 'thread_count', 'time_processing').get(
            pk=task_id)
        task_params['period_from'] = task_params['period_from'].strftime('%Y-%m-%d %H:%M')
        task_params['period_to'] = task_params['period_to'].strftime('%Y-%m-%d %H:%M')
        models.Tasks.objects.filter(pk=task_id).update(force_stop=False)
        celery_id = tasks.run_transcribing_task.delay(task_params)
        models.Tasks.objects.filter(pk=task_id).update(celery_id=celery_id, status=models.TASK_IN_PROGRESS)
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def _stop_task(self, data):
        try:
            task_id = int(data['task_id'])
            task = models.Tasks.objects.get(pk=task_id)
        except (KeyError, models.Tasks.DoesNotExist):
            return {'error': 'No task'}, settings.DEFAULT_ERROR_STATUS
        models.Tasks.objects.filter(pk=task_id).update(status=models.TASK_STOPPED, force_stop=True)
        app.control.revoke(task.celery_id, terminate=True, signal='SIGKILL')
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def show(self):
        languages = models.LanguageList.objects.values('language', 'id').all()
        connections = Connections.objects.filter(db_status_id=ACTIVE_STATUS).values('id', 'alias').all()
        tasks = models.Tasks.objects.values('id', 'period_from', 'period_to', 'alias', 'db__alias',
                                            'language__language',
                                            'status__status', 'percent', 'processed_record_id', 'record_count',
                                            'thread_count', 'time_processing').all()
        context = {
            'languages': languages,
            'connections': connections,
            'tasks': tasks,
        }
        return render_to_string(self.template_name, context)

    def __test_celery_start(self):
        task = models.Tasks.objects.first()
        celery_id = tasks.test_celery_func.delay()
        task.celery_id = celery_id
        task.save()
        # models.Tasks.objects.first().update(celery_id=celery_id)
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def __test_celery_stop(self):
        task = models.Tasks.objects.first()
        app.control.revoke(task.celery_id, terminate=True)
        return {'success': True}, settings.DEFAULT_SUCCESS_STATUS

    def post(self, request, event, data):
        if event == 'add_task':
            response, status = self._add_task(data)
            return JsonResponse(response, status=status)
        if event == 'del_task':
            response, status = self._del_task(data)
            return JsonResponse(response, status=status)
        if event == 'play':
            response, status = self._play_task(data)
            return JsonResponse(response, status=status)
        if event == 'stop':
            response, status = self._stop_task(data)
            return JsonResponse(response, status=status)
        return JsonResponse({'error': 'no event'}, status=settings.DEFAULT_ERROR_STATUS)
