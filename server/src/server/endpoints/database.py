import json

from websockets.sync.server import ServerConnection

from server.base import DefaultRouter

db_router = DefaultRouter()


@db_router.register(path='check-connection')
def check_connection(websocket: ServerConnection):
    response = {'status': True}
    websocket.send(json.dumps(response))
