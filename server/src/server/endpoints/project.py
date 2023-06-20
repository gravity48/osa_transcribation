import json
import time

from settings import STATUS_TIMEOUT
from websockets.exceptions import ConnectionClosed
from websockets.sync.server import ServerConnection

from server.base import DefaultRouter

project_router = DefaultRouter()


@project_router.register(path='start')
def start_task(websocket: ServerConnection):
    response = {'status': True}
    websocket.send(json.dumps(response))


@project_router.register(path='stop')
def stop_task(websocket: ServerConnection):
    response = {'status': True}
    websocket.send(json.dumps(response))


@project_router.register(path='status')
def status_task(websocket: ServerConnection):
    response = {'status': True}
    try:
        while True:
            websocket.send(json.dumps(response))
            time.sleep(STATUS_TIMEOUT)
    except ConnectionClosed:
        return
