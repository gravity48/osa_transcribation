import asyncio
import sys
import signal
import time
import os
import wave
import idb
import io
import copy
import concurrent
import threading
import multiprocessing
import math
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED, ProcessPoolExecutor, \
    as_completed
from collections import namedtuple
from connect_celery.database import PostworkDB
from connect_celery.postgres_db import SettingsDB
from datetime import datetime
from vosk import Model, KaldiRecognizer
from loguru import logger
from multiprocessing.pool import ThreadPool, Pool
from transcribing.models import TranscribingModel
from decoder.decoder import postwork_decoder
'''
ModelTuple = namedtuple('ModelTuple', ['model', 'name'])

WorkProcess = namedtuple('WorkProcess', ['process', 'run_time'])

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

LOG_PATH = 'logfiles/'

FRAMERATE = 16000

SLEEP_TIME = 10

TASK_LIMIT = 100

logger.remove()
log = copy.deepcopy(logger)


class TranscribingTask:
    def control_process(self, event, time_processing, process_list):
        def process_loop():
            for item, work_process in enumerate(process_list):
                if not work_process.process.is_alive():
                    process_list.pop(item)
                    break
                time_delta = datetime.now() - work_process.run_time
                time_live = time_delta.total_seconds()
                if time_live > time_processing:
                    work_process.process.terminate()
                    process_list.pop(item)
                    break
        while not event.is_set():
            force_stop = self.settings_db.get_force_stop(self.settings_record_id)
            if force_stop:
                for item, work_process in enumerate(process_list):
                    work_process.process.terminate()
                return
            process_loop()
        while len(process_list):
            process_loop()

    @staticmethod
    def format_text(f_text, r_text, model_name):
        text_out = f'\r\n -------------{model_name}-------------- '
        text_out += f'\r\nR_Channel: {r_text} \r\nF_Channel: {f_text}'
        return text_out

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.postwork_db_local = PostworkDB(kwargs['server'], kwargs['port'], kwargs['login'], kwargs['password'],
                                            kwargs['db_name'], kwargs['db_system'], kwargs['charset'])
        self.period_to = datetime.strptime(kwargs['period_to'], DATETIME_FORMAT)
        self.period_from = datetime.strptime(kwargs['period_from'], DATETIME_FORMAT)
        self.models = kwargs['models']
        self.thread_count = kwargs['thread_count']
        self.time_processing = kwargs['time_processing']
        logger.remove()
        logfile = kwargs['log']
        # self.log = copy.deepcopy(logger)
        log.add(logfile, format='{time} {level} {message}', level='DEBUG', rotation='5Mb', compression='zip')
        #log.add(sys.stdout, format="{time} {level} {message}", level="INFO")
        if 'write_result' in kwargs:
            self.write_result = True
            self.settings_db = SettingsDB(kwargs['settings_db_login'], kwargs['settings_db_pwd'],
                                          kwargs['settings_db_host'], kwargs['settings_db_name'])
            self.settings_record_id = kwargs['settings_record_id']

    def handle_record(self, record_id, transcribing_models):
        postwork_db = PostworkDB(self.kwargs['server'], self.kwargs['port'], self.kwargs['login'],
                                 self.kwargs['password'],
                                 self.kwargs['db_name'], self.kwargs['db_system'], self.kwargs['charset'])
        postwork_db.mark_record(record_id)
        data = postwork_db.read_data_from_id(record_id)
        speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
        text = ''
        for transcribing_model in transcribing_models:
            f_text, r_text = transcribing_model.model.recognize(speech_decode)
            text += self.format_text(f_text, r_text, transcribing_model.name)
            # text_new = transcribing_model.model.text_from_wav('test123.wav')
        postwork_db.add_comment_to_record(record_id, text)
        log.info(f'Record {record_id} success')
        pass

    def _thread_start(self, records_list: list, thread_id, record_count):
        log.info(f'Run transcribing thread: {thread_id}')
        log.info(f'Train model thread: {thread_id}')
        transcribing_models = []
        for model in self.models:
            transcribing_models.append(ModelTuple(TranscribingModel(model['path']), model['name']))
            transcribing_models[-1].model.train()
        self.settings_db.write_record_count(self.settings_record_id, record_count)
        while len(records_list):
            record_id = records_list.pop(-1)
            log.info(f' Handle record id: {record_id[0]} thread: {thread_id}')
            self.handle_record(record_id[0], transcribing_models)
            print(record_id[0])
            if self.write_result:
                percent = int(((record_count - len(records_list)) * 100) / record_count)
                self.settings_db.write_percent(self.settings_record_id, percent, record_id[0])

    def _transcribing_proj_process(self, record, models):
        self.handle_record(record[0], models)
        pass

    @log.catch
    def run(self):
        log.info('Run transcribing task')
        log.info('Train model')
        transcribing_models = []
        for model in self.models:
            transcribing_models.append(ModelTuple(TranscribingModel(model['path']), model['name']))
            transcribing_models[-1].model.train()
        log.info('Try read data from database')
        while True:
            records_list = self.postwork_db_local.read_records_list(self.period_to, self.period_from)
            record_count = len(records_list)
            log.info(f'Read {record_count} records')
            threads = list()
            for thread_id in range(self.thread_count):
                threads.append(threading.Thread(target=self._thread_start,
                                                args=(records_list, thread_id, record_count)))
                threads[-1].start()
            for thread in threads:
                thread.join()
            if datetime.now() > self.period_to:
                break
            time.sleep(SLEEP_TIME)
        return True

    @log.catch
    def run_with_thread(self, thread_count):
        log.info('Run transcribing thread task')
        log.info('Read data from database')
        while datetime.now() < self.period_to:
            threads = []
            records_list: list = self.postwork_db_local.read_records_list(self.period_to, self.period_from, TASK_LIMIT)
            for thread_id in range(thread_count):
                threads.append(threading.Thread(target=self._thread_start,
                                                args=(records_list, thread_id)))
                threads[-1].start()
            for thread in threads:
                thread.join()
        log.info('Wait files')
        time.sleep(SLEEP_TIME)

    @log.catch
    def run_transcribing_process(self, process_count):
        log.info('Run transcribing process')
        log.info('Read data from database')
        transcribing_models = []
        for model in self.models:
            transcribing_models.append(ModelTuple(TranscribingModel(model['path']), model['name']))
            transcribing_models[-1].model.train()
        log.info('Train transcribing models success')
        records_list, record_count = self.postwork_db_local.read_records_list(self.period_to, self.period_from,
                                                                              TASK_LIMIT)
        self.settings_db.write_record_count(self.settings_record_id, record_count)
        stop_event = threading.Event()
        log.info('Run control thread')
        processes = []
        process_control_thread = threading.Thread(name='process_control', target=self.control_process,
                                                  args=(stop_event, self.time_processing, processes))
        process_control_thread.start()
        log.info('Start process')
        while records_list:
            record = records_list.pop(-1)
            log.info(f'Handle record id: {record[0]}')
            while 1:
                if self.settings_db.get_force_stop(self.settings_record_id):
                    return
                if len(processes) < process_count:
                    work_process = WorkProcess(multiprocessing.Process(target=self._transcribing_proj_process,
                                                                       args=(record, transcribing_models)),
                                               datetime.now())
                    work_process.process.start()
                    processes.append(work_process)
                    break
                if self.write_result:
                    percent = int(((record_count - len(records_list)) * 100) / record_count)
                    self.settings_db.write_percent(self.settings_record_id, percent, record[0])
            if not records_list:
                records_list, record_count = self.postwork_db_local.read_records_list(self.period_to, self.period_from,
                                                                                      TASK_LIMIT)
        log.info('Wait files')
        stop_event.set()
        process_control_thread.join()


if __name__ == '__main__':
    WORK_DIR = '/media/gravity/Data/PycharmProjects/transcribing_web'
    kwargs = {
        'server': '192.168.0.137',
        'port': '3050',
        'db_name': 'd:\\databases\\test_gsm.ibs',
        'login': 'sysdba',
        'password': 'masterkey',
        'db_system': 'Interbase',
        'charset': 'WIN1251',
        'period_from': '2021-09-01 00:00',
        'period_to': '2022-10-31 00:00',
        'models': [{'path': f'{WORK_DIR}/tr_models/model-ru', 'name': 'RU'},
                   {'path': f'{WORK_DIR}/tr_models/vosk-model-uk-v3/vosk-model-uk-v3', 'name': 'UA'}],
        'log': '/media/gravity/Data/PycharmProjects/transcribing_web/logfiles/123.log',
        'write_result': True,
        'settings_db_login': 'django',
        'settings_db_pwd': 'django',
        'settings_db_host': '127.0.0.1',
        'settings_db_name': 'osa_transcribing',
        'settings_record_id': 35,
        'time_processing': 200,
        'thread_count': 5,
    }

    postwork_db = PostworkDB(kwargs['server'], kwargs['port'], kwargs['login'], kwargs['password'],
                             kwargs['db_name'], kwargs['db_system'], kwargs['charset'])
    postwork_db.unmark_all_records(1)

    transcribing_task = TranscribingTask(kwargs)
    transcribing_task.run_transcribing_process(2)
    # transcribing_task.run_transcribing_process(2)
    
    
    
    decoder_speech = transcribing_task.run()

    wav_binary = io.BytesIO(decoder_speech[1])
    wf = wave.open(wav_binary, 'rb')
    print(wf.getnchannels())
    print(wf.getsampwidth())
    print(wf.getcomptype())
    print(wf.getframerate())

    con = idb.connect(dsn='172.16.71.134:c:\\Databases\\TESTOVAYA_EMPTY.IBS', user='sysdba', password='masterkey',
                      charset='WIN1251', fb_library_name='/lib/i386-linux-gnu/libgds.so')

    cur = con.cursor()
    # Execute the SELECT statement:
    cur.execute("select * from spr_event")
    result = cur.fetchall()
    print(result)
    if not os.path.exists("model-ru"):
        print(
            "Please download the model from https://github.com/alphacep/kaldi-android-demo/releases and unpack as 'model-en' in the current folder.")
        exit(1)

pass
'''
