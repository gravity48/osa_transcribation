from settings import SERVER_HOST, SERVER_PORT
from websockets.sync.server import serve

from server.server import TranscribingServer

if __name__ == '__main__':
    with serve(TranscribingServer().handler, SERVER_HOST, SERVER_PORT) as server:
        server.serve_forever()
