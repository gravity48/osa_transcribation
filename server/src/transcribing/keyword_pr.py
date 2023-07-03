import io
import wave
from multiprocessing import Queue, Value
from typing import Dict, List

from connect_celery.database import PostworkDB
from decoder.decoder import postwork_decoder
from loguru import logger
from recognize_func import get_durations, search_keywords_in_set
from vosk_server import VoskServer


def keyword_identification_process(
    queue: Queue,
    is_run: Value,
    db: Dict,
    models: List[Dict],
    alias: Dict,
    item: int,
    record_processed: Value,
    active_time: int,
    keywords: List,
    percent: float,
    debug=False,
):
    TRAIN_MODELS = []

    def format_text_list(words_list):
        text = ''
        for word in words_list:
            text += f'{word} '
        return text

    def keyword_from_chunks(chunks):
        words_chunks = set()
        if not chunks:
            return []
        for chunk in chunks:
            stream = io.BytesIO()
            chunk.export(stream, format='wav')
            chunk_wav = wave.open(stream, 'rb')
            for train_model in TRAIN_MODELS:
                words = train_model.recognize_keyword(chunk_wav, percent, keywords)
                words_chunks.update(words)
            chunk_wav.close()
        return words_chunks

    for model in models:
        train_model = VoskServer(model['ip'], model['port'])
        TRAIN_MODELS.append(train_model)

    postwork_db = PostworkDB(**db)
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
            f_words = keyword_from_chunks(chunks[0])
            r_words = keyword_from_chunks(chunks[1])
            words = f_words.union(r_words)
            find_keywords = search_keywords_in_set(keywords, words)
            postwork_db.mark_record_find_keyword(record_id, find_keywords)
            '''
            comment = ''
            for word in words:
                comment += f'{word} '
            postwork_db.add_comment_to_record(record_id, comment)
            '''
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
            if debug:
                break
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error: {error}')
