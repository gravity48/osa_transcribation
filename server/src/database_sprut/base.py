from contextlib import contextmanager


class SpeechBlob(bytes):
    ...


class BaseModels:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AbstractDBProvider:
    def __init__(
        self,
        ip: str,
        port: int,
        db_login: str,
        db_password: str,
        db_name: str,
    ):
        self.ip = ip
        self.port = port
        self.db_login = db_login
        self.db_password = db_password
        self.db_name = db_name

    @contextmanager
    def session(self):
        raise NotImplementedError

    def try_connection(self):
        raise NotImplementedError
