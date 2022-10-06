import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 4848  # The port used by the server


class TranscriptionServer:
    ATTEMPTS_COUNT = 10
    SOCKET_BUFFER = 10000

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def __del__(self):
        self.s.close()
        del self.s

    def send(self, context):
        request = json.dumps(context, ensure_ascii=False).encode('utf8')
        header = len(request).to_bytes(4, byteorder='big')
        request = header + request
        self.s.sendall(request)

    def resv(self):
        data = b""
        iteration = 0
        try:
            pckg_lng_byte = self.s.recv(4)
            package_lng = int.from_bytes(pckg_lng_byte, byteorder='big')
            while iteration < self.ATTEMPTS_COUNT:
                iteration += iteration  # increment iter number
                buffer: bytes = self.s.recv(self.SOCKET_BUFFER)
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

    def check_connection(self, context):
        context['event'] = 'check_connection'
        self.send(context)
        request = self.resv()
        try:
            status = request['status']
            return status
        except (KeyError, TypeError):
            return False

    def start_task(self, context):
        context['event'] = 'start_task'
        self.send(context)
        request = self.resv()
        try:
            status = request['status']
            return status
        except (KeyError, TypeError):
            return False

    def stop_task(self, context):
        context['event'] = 'stop_task'
        self.send(context)
        request = self.resv()
        try:
            status = request['status']
            return status
        except (KeyError, TypeError):
            return False

    def status_task(self, context):
        context['event'] = 'status_task'
        self.send(context)
        request = self.resv()
        try:
            status = request['status']
            return status
        except (KeyError, TypeError):
            return False
