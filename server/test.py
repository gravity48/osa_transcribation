import datetime
from connect_celery.database import PostworkDB
from loguru import logger
from start import pause_identification_process, transcribing_process, keyword_identification_process
from multiprocessing import Pool, Process, Queue, Semaphore, Value

if __name__ == '__main__':
    alias = '123'
    db = {
        'ip': '127.0.0.1',
        'port': '5432',
        'db_login': 'admin',
        'db_password': '000092',
        'db_name': 'test_sprut',
        'db_system': {
            'name': 'Postgres'
        }
    }
    models = [
        {
            'path': 'model-ru',
            'short_name': 'RU',
            'ip': 'localhost',
            'port': 2700
        },

        {
            'path': 'model-ua',
            'short_name': 'UA',
            'ip': 'localhost',
            'port': 2701
        }
    ]
    option_task = {
        'speech_time': 3,
        'keywords': 'привет\nхарьков\nдоброе',
    }
    option_connections = {
    }
    keywords = option_task['keywords'].split('\n')
    logger.add(alias, filter=lambda record: alias in record["extra"], format="{time} {level} {message}",
               level="INFO")
    db_postwork = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
    period_from = datetime.datetime.strptime('2022-09-01T02:00:01+03:00', '%Y-%m-%dT%H:%M:%S%z')
    period_to = datetime.datetime.strptime('2022-11-30T02:00:01+03:00', '%Y-%m-%dT%H:%M:%S%z')
    db_postwork.unmark_all_records(1)
    records, record_count = db_postwork.read_records_list(period_to, period_from, option_connections, 100, 0)
    # records = [(4, 0), ]
    queue = Queue()
    is_run = Value('i', 1)
    records_processed = Value('i', 0)
    for record_id in records:
        queue.put(22)
        keyword_identification_process(queue, is_run, db, models, {alias: True}, 1, records_processed, 2, keywords, 0.01)
        #transcribing_process(queue, is_run, db, models, {alias: True}, 1, records_processed, 2)
        #pause_identification_process(queue, is_run, db, {alias: True}, 1, records_processed, 2)
