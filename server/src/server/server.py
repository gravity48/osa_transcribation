import json
import re

from websockets.sync.server import ServerConnection

from server.exceptions import RouteNotFoundError
from server.router import router as default_router


class TranscribingServer:
    router = default_router

    @staticmethod
    def _send_error(websocket: ServerConnection, msg):
        response = {
            'error': msg,
        }
        websocket.send(json.dumps(response))

    @staticmethod
    def _get_path(path: str) -> str:
        match = re.search(r'^\/(?P<path>[a-z-]+)\/', path)
        if match:
            return match.group('path')
        else:
            raise RouteNotFoundError()

    def handler(self, websocket: ServerConnection):
        try:
            path = self._get_path(websocket.request.path)
            endpoint = self.router.get_endpoint(path)
            endpoint(websocket)
        except RouteNotFoundError:
            self._send_error(websocket, 'router undefined')
