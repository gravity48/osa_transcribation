import json
import time
import threading
import sys
import socketserver
import multiprocessing
from collections import namedtuple
from connect_celery.database import PostworkDB
from connect_celery.postgres_db import SettingsDB
from decoder.decoder import postwork_decoder
from datetime import datetime
from loguru import logger
from models import TranscribingModel
from multiprocessing import Pool, Process, Queue, Semaphore, Value
from custom_process import CustomProcess

ModelTuple = namedtuple('ModelTuple', ['model', 'name'])

WorkProcess = namedtuple('WorkProcess', ['process', 'run_time'])

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

LOG_PATH = 'logs/'

MODEL_PATH = 'models/'


def transcribing_process(queue, is_run, db, models, alias, item, record_processed):
    def format_text(f_text, r_text, model_name):
        text_out = f'\r\n -------------{model_name}-------------- '
        text_out += f'\r\nR_Channel: {r_text} \r\nF_Channel: {f_text}'
        return text_out

    model_path = MODEL_PATH + models['path']
    model = TranscribingModel(model_path)
    model.train()
    postwork_db = PostworkDB(db['ip'], db['port'], db['db_login'], db['db_password'], db['db_name'], db['db_system'])
    while is_run.value:
        record_id = queue.get()
        try:
            postwork_db.mark_record(record_id)
            data = postwork_db.read_data_from_id(record_id)
            speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
            text = ''
            f_text, r_text = model.recognize(speech_decode)
            text += format_text(f_text, r_text, models['short_name'])
            # text_new = transcribing_model.model.text_from_wav('test123.wav')
            postwork_db.add_comment_to_record(record_id, text)
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} success')
            record_processed.value = record_processed.value + 1
        except Exception as e:
            logger.bind(**alias).info(f'Thread: {item} Record {record_id} error')
            continue


def control_process(queue, is_run, db_init, period_from, period_to, *args, **kwargs):
    limit = 10
    db = PostworkDB(db_init['ip'], db_init['port'], db_init['db_login'], db_init['db_password'],
                    db_init['db_name'], db_init['db_system'])
    period_from = datetime.strptime(period_from, '%Y-%m-%dT%H:%M:%S')
    period_to = datetime.strptime(period_to, '%Y-%m-%dT%H:%M:%S')
    records_list, record_count = db.read_records_list(period_to, period_from, db_init['options'], limit)
    while records_list:
        record = records_list.pop(-1)
        db.mark_record_in_queue(record[0])
        queue.put(record[0])
        while 1:
            if queue.qsize() < limit:
                break
            time.sleep(10)
        if not records_list:
            records_list, record_count = db.read_records_list(period_to, period_from, db_init['options'], limit)


class TranscribingTask:
    FRAMERATE = 16000
    SLEEP_TIME = 10
    TASK_LIMIT = 100

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
            'record_processed': self.records_processed.value
        }
        return context

    def _speaker_identification_task(self, record_id, model: ModelTuple, spk_vector):
        postwork_db = PostworkDB(self.kwargs['server'], self.kwargs['port'], self.kwargs['login'],
                                 self.kwargs['password'],
                                 self.kwargs['db_name'], self.kwargs['db_system'], self.kwargs['charset'])
        data = postwork_db.read_data_from_id(record_id)
        speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
        vector_r, vector_f = model.model.get_vectors_from_data(speech_decode)
        result = model.model.cosine_dist(vector_f, spk_vector)
        pass

    def transcribing(self):
        logger.bind(**self.alias).info('Run transcribing')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        is_run = Value('i', 1)
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(target=transcribing_process,
                        args=(queue, is_run, self.db_init, self.models, self.alias, item, self.records_processed)))
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(target=control_process,
                                       args=(queue, is_run, self.db_init, self.period_from, self.period_to))
        self.control_process.start()

    def run_speaker_identification_process(self, process_count, filepath):
        logger.info('Run speaker identification process')
        logger.info('Train models')
        transcribing_model = ModelTuple(TranscribingModel(self.models[0]['path']), self.models[1]['name'])
        transcribing_model.model.train()
        transcribing_model.model.set_spk_models(self.spk_model)
        logger.info('Train transcribing models success')
        logger.info('Get spk vector')
        spk_vector = transcribing_model.model.get_speaker_vector(filepath)
        records_list, record_count = self.postwork_db_local.read_records_list(self.period_to, self.period_from,
                                                                              self.TASK_LIMIT)
        while records_list:
            record = records_list.pop(-1)
            logger.info(f'Handle record id: {record[0]}')
            self._speaker_identification_task(record[0], transcribing_model, spk_vector)
        pass


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

    def status_task(self, data):
        transcribing_task = self.TASK_RUNNING.pop(data['id'], None)
        if transcribing_task:
            context = transcribing_task.status()
            self.send(context)
        else:
            self.send_error('no tasks')

    def handle(self) -> None:
        event = ''
        try:
            data_json: dict = self.recv()
            event = data_json.pop('event')
        except KeyError:
            self.send_error('Command parse error')
            return
        if event == 'check_connection':
            self.check_connection(data_json)
        if event == 'start_task':
            self.start_task(data_json)
        if event == 'stop_task':
            self.stop_task(data_json)
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
