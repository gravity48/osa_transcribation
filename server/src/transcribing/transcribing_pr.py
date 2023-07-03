import io
import wave

from connect_celery.database import PostworkDB
from decoder.decoder import postwork_decoder
from loguru import logger
from recognize_func import format_text, get_durations
from vosk_server import VoskServer


def transcribing_process(queue, is_run, db, models, alias, item, record_processed, active_time):
    TRAIN_MODELS = []

    def text_from_chunks(chunks):
        text_chunks = ''
        if not chunks:
            return ''
        for chunk in chunks:
            stream = io.BytesIO()
            chunk.export(stream, format='wav')
            chunk_wav = wave.open(stream)
            conf_chunk = 0
            text_chunk = ''
            for train_model in TRAIN_MODELS:
                conf, text = train_model.recognize_chunk(chunk_wav)
                if conf > conf_chunk:
                    text_chunk = text
                    conf_chunk = conf
            if text_chunk:
                text_chunks += f'{text_chunk}  '
            chunk_wav.close()
        return text_chunks

    for model in models:
        train_model = VoskServer(model['ip'], model['port'])
        TRAIN_MODELS.append(train_model)

    postwork_db = PostworkDB(
        db['ip'],
        db['port'],
        db['db_login'],
        db['db_password'],
        db['db_name'],
        db['db_system'],
    )
    while is_run.value:
        record_id = queue.get()
        try:
            postwork_db.mark_record(record_id)
            data = postwork_db.read_data_from_id(record_id)
            speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
            status, chunks = get_durations(speech_decode[0], speech_decode[1], active_time)
            if not status:
                postwork_db.mark_record_empty(record_id)
                continue
            f_text = text_from_chunks(chunks[0])
            r_text = text_from_chunks(chunks[1])
            text = format_text(f_text, r_text, 'Транскрибация')
            # text_new = transcribing_model.model.text_from_wav('test123.wav')
            postwork_db.add_comment_to_record(record_id, text)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error: {error}')
