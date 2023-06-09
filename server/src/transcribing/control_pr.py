import time
from datetime import datetime

from loguru import logger

from connect_celery.database import PostworkDB


def control_process(queue, is_run, db_init, period_from, period_to, alias, *args, **kwargs):
    db = PostworkDB(db_init['ip'], db_init['port'], db_init['db_login'], db_init['db_password'],
                    db_init['db_name'], db_init['db_system'])
    period_from = datetime.strptime(period_from, '%Y-%m-%dT%H:%M:%S%z')
    period_to = datetime.strptime(period_to, '%Y-%m-%dT%H:%M:%S%z')
    limit = 100
    records_list = []
    while is_run:
        try:
            while 1:
                if queue.qsize() < limit:
                    break
                time.sleep(5)
            records, record_count = db.read_records_list(period_to, period_from, db_init['options'], 1)
            while not records:
                records, record_count = db.read_records_list(period_to, period_from, db_init['options'], 1)
                time.sleep(5)
            records_list += records
            record = records_list.pop(-1)
            db.mark_record_in_queue(record[0])
            queue.put(record[0])
            logger.bind(**alias).info(f'Add {record[0]} to queue')
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Read from database error {error}')
            time.sleep(5)
