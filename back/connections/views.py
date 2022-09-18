import django, datetime, json
import os
from django.db.models import F
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse, Http404, HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import generic
from django.shortcuts import render
from django.utils.decorators import method_decorator
from functools import wraps
from . import models, forms, tasks

event_list = {'add_connection', 'del_connection'}


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
class ConnectionsView(generic.View):
    template_name = 'connections/connections.html'

    @staticmethod
    def _add_connection(data):
        connection_form = forms.ConnectionForm(data)
        if connection_form.is_valid():
            registered_db = models.Connections(**connection_form.cleaned_data)
            registered_db.save()
            connect_struct = models.Connections.objects.values('ip', 'port', 'db_system__name', 'db_login',
                                                               'db_password',
                                                               'db_name').filter(pk=registered_db.id).first()
            tasks.connect_to_db.delay(connect_struct['ip'], connect_struct['port'], connect_struct['db_system__name'],
                                      connect_struct['db_name'],
                                      connect_struct['db_login'], connect_struct['db_password'], registered_db.id)
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            errors = json.loads(connection_form.errors.as_json())
            return errors, settings.DEFAULT_ERROR_STATUS

    @staticmethod
    def _del_connection(data):
        del_con_form = forms.DelConnectionForm(data)
        if del_con_form.is_valid():
            con_id = del_con_form.cleaned_data['con_id']
            models.Connections.objects.get(pk=con_id).delete()
            return {'success': True}, settings.DEFAULT_SUCCESS_STATUS
        else:
            errors = json.loads(del_con_form.errors.as_json())
            return errors, settings.DEFAULT_ERROR_STATUS

    def show(self):
        db_systems = models.DatabaseSystems.objects.all()
        connections = models.Connections.objects.annotate(system=F('db_system__name'),
                                                          status=F('db_status__status_name')).values('id', 'alias',
                                                                                                     'ip',
                                                                                                     'db_name',
                                                                                                     'db_status',
                                                                                                     'system',
                                                                                                     'status').all()
        context = {
            'db_systems': db_systems,
            'connections': connections,
        }
        return render_to_string(self.template_name, context)

    def post(self, request, event, data):
        if event == 'add_connection':
            response, status = self._add_connection(data)
            return JsonResponse(response, status=status)
        if event == 'del_connection':
            response, status = self._del_connection(data)
            return JsonResponse(response, status=status)
        return JsonResponse({'error': 'no event'}, status=settings.DEFAULT_ERROR_STATUS)
