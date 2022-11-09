import io
import json
import time
import threading
import sys
import socketserver
import multiprocessing
import wave
from collections import namedtuple
from connect_celery.database import PostworkDB
from connect_celery.postgres_db import SettingsDB
from decoder.decoder import postwork_decoder
from datetime import datetime
from loguru import logger
from models import TranscribingModel
from vosk_server import VoskServer
from multiprocessing import Pool, Process, Queue, Semaphore, Value
from recognize_func import get_durations, get_duration, format_text, search_keywords_in_list

ModelTuple = namedtuple('ModelTuple', ['model', 'name'])

WorkProcess = namedtuple('WorkProcess', ['process', 'run_time'])

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

LOG_PATH = 'logs/'

MODEL_PATH = 'models/'

KeywordsIdentificationsTaskType = 3
PauseIdentificationTaskType = 2
TranscribingTaskType = 1


def pause_identification_process(queue, is_run, db, alias, item, record_processed, time_min):
    postwork_db = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
    while is_run.value:
        record_id = queue.get()
        try:
            postwork_db.mark_record(record_id)
            data = postwork_db.read_data_from_id(record_id)
            f_speech, r_speech = postwork_decoder(data[0][0], data[0][1], data[0][2])
            f_wav_duration = get_duration(f_speech)
            r_wav_duration = get_duration(r_speech)
            if (f_wav_duration < time_min) and (r_wav_duration < time_min):
                postwork_db.mark_record_empty(record_id)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error:  {error}')
        continue


def transcribing_process(queue, is_run, db, models, alias, item, record_processed, active_time):
    TRAIN_MODELS = []

    def text_from_chunks(chunks):
        text_chunks = ''
        if not chunks:
            return ''
        for chunk in chunks:
            stream = io.BytesIO()
            chunk.export(stream, format='wav')
            chunk_wav = stream.getvalue()
            conf_chunk = 0
            text_chunk = ''
            for train_model in TRAIN_MODELS:
                conf, text = train_model.recognize_chunk(chunk_wav)
                if conf > conf_chunk:
                    text_chunk = text
                    conf_chunk = conf
            if text_chunk:
                text_chunks += f'{text_chunk}  '
        return text_chunks

    for model in models:
        train_model = VoskServer(model['ip'], model['port'])
        TRAIN_MODELS.append(train_model)

    postwork_db = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
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
            continue


def keyword_identification_process(queue, is_run, db, models, alias, item, record_processed, active_time, keywords,
                                   percent):
    TRAIN_MODELS = []

    def format_text_list(words_list):
        text = ''
        for word in words_list:
            text += f'{word} '
        return text

    def keyword_from_chunks(chunks):
        words_chunks = []
        if not chunks:
            return []
        for chunk in chunks:
            stream = io.BytesIO()
            chunk.export(stream, format='wav')
            chunk_wav = wave.open(stream, 'rb')
            for train_model in TRAIN_MODELS:
                words = train_model.recognize_keyword(chunk_wav, percent, keywords)
                words_chunks += words
            chunk_wav.close()
        return words_chunks

    for model in models:
        train_model = VoskServer(model['ip'], model['port'])
        TRAIN_MODELS.append(train_model)

    postwork_db = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
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
            words = f_words + r_words
            find_keywords = search_keywords_in_list(keywords, words)
            postwork_db.mark_record_find_keyword(record_id, find_keywords)
            '''
            comment = ''
            for word in words:
                comment += f'{word} '
            postwork_db.add_comment_to_record(record_id, comment)
            '''
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error: {error}')
            continue


def control_process(queue, is_run, db_init, period_from, period_to, alias, *args, **kwargs):
    db = PostworkDB(db_init['ip'], db_init['port'], db_init['db_login'], db_init['db_password'],
                    db_init['db_name'], db_init['db_system'])
    period_from = datetime.strptime(period_from, '%Y-%m-%dT%H:%M:%S')
    period_to = datetime.strptime(period_to, '%Y-%m-%dT%H:%M:%S')
    limit = 100
    records_list = []
    while is_run:
        try:
            records, record_count = db.read_records_list(period_to, period_from, db_init['options'], 1)
            while not records:
                records, record_count = db.read_records_list(period_to, period_from, db_init['options'], 1)
                time.sleep(5)
            records_list += records
            record = records_list.pop(-1)
            db.mark_record_in_queue(record[0])
            queue.put(record[0])
            logger.bind(**alias).info(f'Add {record[0]} to queue')
            while 1:
                if queue.qsize() < limit:
                    break
                time.sleep(5)
        except Exception as e:
            error = repr(e)
            logger.bind(**alias).info(f'Read from database error {error}')
            time.sleep(5)
            continue

class TranscribingTask:
    FRAMERATE = 16000
    SLEEP_TIME = 10
    TASK_LIMIT = 100

    @staticmethod
    def options_parse(options):
        keywords = options.get('keywords', [])
        if keywords:
            keywords = keywords.split('\n')
        try:
            percent = options['recognize_percent']
            percent /= 100
        except KeyError:
            percent = 0.9
        return keywords, percent

    def __init__(self, db, model, task_type, alias, period_from, period_to, thread_count,
                 time_processing, options, *args, **kwargs):
        self.db_init = db
        self.period_to = period_to
        self.period_from = period_from
        self.models = model
        self.thread_count = thread_count
        self.time_processing = time_processing
        self.alias = {alias: True}
        self.options = options
        self.keywords, self.percent = self.options_parse(self.options)
        # self.spk_model = kwargs['spk_model']
        self.log = f'logs/{alias}.log'
        logger.add(self.log, filter=lambda record: alias in record["extra"], format="{time} {level} {message}",
                   level="INFO")
        self.process_pool = []
        self.control_process = None
        self.records_processed = Value('i', 0)

    def stop(self):
        self.control_process.kill()
        for process in self.process_pool:
            process.kill()

    def status(self):
        context = {
            'record_processed': self.records_processed.value,
            'is_running': True,
        }
        return context

    def transcribing(self):
        logger.bind(**self.alias).info('Run transcribing')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        is_run = Value('i', 1)
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(target=transcribing_process,
                        args=(queue, is_run, self.db_init, self.models, self.alias, item, self.records_processed,
                              self.options['speech_time'])))
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(target=control_process,
                                       args=(queue, is_run, self.db_init, self.period_from, self.period_to, self.alias))
        self.control_process.start()

    def pause_identification(self):
        logger.bind(**self.alias).info('Run pause identification')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        is_run = Value('i', 1)
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(target=pause_identification_process,
                        args=(queue, is_run, self.db_init, self.alias, item, self.records_processed,
                              self.options['speech_time'])))
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(target=control_process,
                                       args=(queue, is_run, self.db_init, self.period_from, self.period_to))
        self.control_process.start()
        pass

    def search_keywords(self):
        logger.bind(**self.alias).info('Run search keywords')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        is_run = Value('i', 1)
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(target=keyword_identification_process,
                        args=(queue, is_run, self.db_init, self.models, self.alias, item, self.records_processed,
                              self.options['speech_time'], self.keywords, self.percent)))
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(target=control_process,
                                       args=(queue, is_run, self.db_init, self.period_from, self.period_to, self.alias))
        self.control_process.start()


class TranscribingServer(socketserver.BaseRequestHandler):
    SOCKET_BUFFER = 10000
    ATTEMPTS_COUNT = 10
    TASK_RUNNING = {}

    def send_error(self, error_text: str):
        logger.debug(error_text)
        context = {
            'error': error_text,
        }
        self.send(context)

    def send(self, context):
        request = json.dumps(context, ensure_ascii=False).encode('utf8')
        header = len(request).to_bytes(4, byteorder='big')
        request = header + request
        self.request.sendall(request)

    def recv(self):
        data = b""
        iteration = 0
        try:
            pckg_lng_byte = self.request.recv(4)
            package_lng = int.from_bytes(pckg_lng_byte, byteorder='big')
            while iteration < self.ATTEMPTS_COUNT:
                iteration += iteration  # increment iter number
                buffer: bytes = self.request.recv(self.SOCKET_BUFFER)
                data += buffer
                if len(data) == package_lng:
                    data_string = buffer.decode("utf-8")
                    data_json = json.loads(data_string)
                    del buffer
                    return data_json
        except UnicodeError:
            self.send_error('Unicode Error')
        except json.decoder.JSONDecodeError:
            self.send_error('JSON Error')

    def check_connection(self, data):
        status = PostworkDB(**data).try_connection()
        context = {
            'status': status
        }
        self.send(context)

    def start_task(self, data):
        logger.info(data)
        trascribing_task = TranscribingTask(**data)
        if data['task_type']['id'] == TranscribingTaskType:
            trascribing_task.transcribing()
        if data['task_type']['id'] == PauseIdentificationTaskType:
            trascribing_task.pause_identification()
        if data['task_type']['id'] == KeywordsIdentificationsTaskType:
            trascribing_task.search_keywords()
        self.TASK_RUNNING[data['id']] = trascribing_task
        context = {
            'status': True
        }
        self.send(context)

    def pause_del_task(self, data):
        trascribing_task = TranscribingTask(**data)
        trascribing_task.transcribing()
        self.TASK_RUNNING[data['id']] = trascribing_task
        context = {
            'status': True
        }
        self.send(context)

    def stop_task(self, data_json):
        transcribing_task = self.TASK_RUNNING.pop(data_json['id'], None)
        if transcribing_task:
            transcribing_task.stop()
            del transcribing_task
        self.send({'status': True})

    def status(self, data):
        response = {}
        for task_id in data['task_run']:
            try:
                transcribing_task = self.TASK_RUNNING[task_id]
                context = transcribing_task.status()
                response[task_id] = context
            except KeyError:
                response[task_id] = {'is_running': False}
        self.send(response)

    def handle(self) -> None:
        event = ''
        try:
            data_json: dict = self.recv()
            event = data_json.pop('event')
        except (KeyError, AttributeError):
            self.send_error('Command parse error')
            return
        if event == 'check_connection':
            self.check_connection(data_json)
            return
        if event == 'start_task':
            self.start_task(data_json)
            return
        if event == 'stop_task':
            self.stop_task(data_json)
            return
        if event == 'status':
            self.status(data_json)
            return
        self.send_error('unknown event')
        return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 4848
    logger.info('Run server')

    server = ThreadedTCPServer((HOST, PORT), TranscribingServer)

    with server:
        ip, port = server.server_address
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        logger.info(f'Server loop running in thread: {server_thread.name}')
        server_thread.join()
pass
