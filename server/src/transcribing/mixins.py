from database_sprut.factory import SprutDBFactory
from services.sprut import SprutService


class SetupSprutMixin:
    def setup_database(
        self,
        host: str,
        port: int,
        login: str,
        password: str,
        path: str,
        provider_name: str,
    ):
        db = SprutDBFactory().get_db_provider(provider_name)
        db = db(host, port, login, password, path)
        self.sprut_service = SprutService(db.session)
