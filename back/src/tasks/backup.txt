import signal
import time
from celery import shared_task
from django.conf import settings
from transcribing.start import TranscribingTask
from . import models

DATETIME_FORMAT = '%Y-%m-%d %H:%M'


@shared_task(acks_late=True)
def run_transcribing_task(task_params):
    kwargs = {
        'server': task_params['db__ip'],
        'port': task_params['db__port'],
        'db_name': task_params['db__db_name'],
        'login': task_params['db__db_login'],
        'password': task_params['db__db_password'],
        'db_system': task_params['db__db_system__name'],
        'charset': 'WIN1251',
        'period_from': task_params['period_from'],
        'period_to': task_params['period_to'],
        'models': [{'path': settings.MODELSDIR + task_params['language__model'], 'name': task_params['language__short_name']}, ],
        'log': settings.LOGDIR + task_params['log'],
        'write_result': True,
        'settings_db_login': settings.DATABASES['default']['USER'],
        'settings_db_pwd': settings.DATABASES['default']['PASSWORD'],
        'settings_db_host': settings.DATABASES['default']['HOST'],
        'settings_db_name': settings.DATABASES['default']['NAME'],
        'settings_record_id': task_params['id'],
        'thread_count': task_params['thread_count'],
        'time_processing': task_params['time_processing'],
    }
    transcribing_task = TranscribingTask(kwargs)
    transcribing_task.run_transcribing_process(kwargs['thread_count'])
    pass


@shared_task
def test_celery_func():
    for i in range(10):
        print(f'sleep {i}')
        time.sleep(5)

