<<<<<<< HEAD
import json
import socketserver
import threading
from collections import namedtuple
from json import JSONDecodeError

from connect_celery.database import PostworkDB
from loguru import logger
from settings import SERVER_HOST, SERVER_PORT
from transcribing.manager import TranscribingTask

ModelTuple = namedtuple('ModelTuple', ['model', 'name'])

WorkProcess = namedtuple('WorkProcess', ['process', 'run_time'])

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

LOG_PATH = 'logs/'

KeywordsIdentificationsTaskType = 3
PauseIdentificationTaskType = 2
TranscribingTaskType = 1


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
        except JSONDecodeError:
            self.send_error('JSON Error')

    def check_connection(self, data):
        status = PostworkDB(**data).try_connection()
        context = {'status': status}
        self.send(context)

    def start_task(self, data):
        logger.info(data)
        transcribing_task = TranscribingTask(**data)
        if data['task_type']['id'] == TranscribingTaskType:
            transcribing_task.transcribing()
        if data['task_type']['id'] == PauseIdentificationTaskType:
            transcribing_task.pause_identification()
        if data['task_type']['id'] == KeywordsIdentificationsTaskType:
            transcribing_task.search_keywords()
        self.TASK_RUNNING[data['id']] = transcribing_task
        context = {'status': True}
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
=======
from settings import SERVER_HOST, SERVER_PORT
from websockets.sync.server import serve
>>>>>>> e64f36e (server refactoring)

from server.server import TranscribingServer

if __name__ == '__main__':
    with serve(TranscribingServer().handler, SERVER_HOST, SERVER_PORT) as server:
        server.serve_forever()
