from celery import shared_task
from connect_celery.database import PostworkDB
from connections.models import Connections
from . import models


@shared_task
def connect_to_db(ip, port, db_system, db_name, db_login, db_password, con_id):
    postwork_db = PostworkDB(ip, port, db_login, db_password, db_name, db_system)
    status = postwork_db.try_connection()
    if status:
        active_status = models.ConnectionsStatus.objects.get(status_name='Active')
        models.Connections.objects.filter(pk=con_id).update(db_status=active_status)
    return True




