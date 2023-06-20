from typing import Type

from database_sprut.base import AbstractDBProvider
from database_sprut.db.postgres import PostgresSprutDatabase


class SprutDBFactory:
    def __init__(self):
        self._providers = {
            'Postgres': PostgresSprutDatabase,
            'default': PostgresSprutDatabase,
        }

    def get_db_provider(self, provider_name) -> Type[AbstractDBProvider]:
        provider = self._providers.get(provider_name, self._providers['default'])
        return provider
