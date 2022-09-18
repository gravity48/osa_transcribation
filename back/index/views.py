import django, datetime, json
import os
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
from connections.views import ConnectionsView
from tasks.views import TasksView

event_list = ['show_connections', 'show_tasks']


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


@method_decorator(login_required, name='get')
@method_decorator(post_decorators, name='post')
class IndexView(generic.View):
    template_name = 'index/index.html'

    @staticmethod
    def _show_connections():
        connect_view = ConnectionsView()
        context = {
            'success': True,
            'render_content': connect_view.show(),
        }
        return context, settings.DEFAULT_SUCCESS_STATUS

    @staticmethod
    def _show_tasks():
        tasks_view = TasksView()
        context = {
            'success': True,
            'render_content': tasks_view.show(),
        }
        return context, settings.DEFAULT_SUCCESS_STATUS

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest, event: str, data):
        if event == 'show_connections':
            response, status = self._show_connections()
            return JsonResponse(response, status=status)
        if event == 'show_tasks':
            response, status = self._show_tasks()
            return JsonResponse(response, status=status)
        return JsonResponse({'error': 'no event'}, status=settings.DEFAULT_ERROR_STATUS)




