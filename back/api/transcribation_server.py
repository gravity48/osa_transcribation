import socket
import json
from functools import wraps

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 4848  # The port used by the server

def error_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (KeyError, TypeError):
            return False, {'transcribing_server': 'Попробуйте снова'}
        except ConnectionRefusedError:
            return False, {'transcribing_server': 'Сервер недоступен'}
    return wrapper


class TranscriptionServer:
    ATTEMPTS_COUNT = 10
    SOCKET_BUFFER = 10000

    def __init__(self, host='127.0.0.1', port=4848):
        self.host = host
        self.port = port

    def send(self, s, context):
        request = json.dumps(context, ensure_ascii=False).encode('utf8')
        header = len(request).to_bytes(4, byteorder='big')
        request = header + request
        s.sendall(request)

    def resv(self, s):
        data = b""
        iteration = 0
        try:
            pckg_lng_byte = s.recv(4)
            package_lng = int.from_bytes(pckg_lng_byte, byteorder='big')
            while iteration < self.ATTEMPTS_COUNT:
                iteration += iteration  # increment iter number
                buffer: bytes = s.recv(self.SOCKET_BUFFER)
                data += buffer
                if len(data) == package_lng:
                    data_string = buffer.decode("utf-8")
                    data_json = json.loads(data_string)
                    del buffer
                    return data_json
        except (json.JSONDecodeError, KeyError):
            return None
        except UnicodeError:
            return None

    @error_wrap
    def check_connection(self, context):
        context['event'] = 'check_connection'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.send(s, context)
            request = self.resv(s)
            status = request['status']
            return status, {'alias': context['alias']}

    @error_wrap
    def start_task(self, context):
        context['event'] = 'start_task'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.send(s, context)
            request = self.resv(s)
            status = request['status']
            return status, request

    @error_wrap
    def stop_task(self, context):
        context['event'] = 'stop_task'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.send(s, context)
            request = self.resv(s)
            status = request['status']
            return status, request

    @error_wrap
    def status_task(self, context):
        context['event'] = 'status'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.send(s, context)
            request = self.resv(s)
            return True, request
