from loguru import logger

from connect_celery.database import PostworkDB
from decoder.decoder import postwork_decoder
from recognize_func import get_durations


def pause_identification_process(queue, is_run, db, alias, item, record_processed, time_min):
    postwork_db = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
    while is_run.value:
        record_id = queue.get()
        try:
            postwork_db.mark_record(record_id)
            data = postwork_db.read_data_from_id(record_id)
            speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
            status, chunks = get_durations(speech_decode[0], speech_decode[1], time_min)
            if not status:
                postwork_db.mark_record_empty(record_id)
                continue
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error:  {error}')
        continue
