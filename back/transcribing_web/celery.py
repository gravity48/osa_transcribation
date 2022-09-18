import os

from celery import Celery
from celery.signals import worker_shutting_down
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcribing_web.settings')

app = Celery('transcribing_web', broker='amqp://user:000092@172.17.0.1:5672')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


'''
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    #sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(minute=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)
    
'''
