from contextlib import contextmanager

from database_sprut.base import AbstractDBProvider
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()


class PostgresSprutDatabase(AbstractDBProvider):
    def __init__(self, *args, **kwargs):
        super(PostgresSprutDatabase, self).__init__(*args, **kwargs)
        connection_str = (
            f'postgresql+psycopg2://'
            f'{self.db_login}:{self.db_password}@'
            f'{self.ip}:{self.port}/{self.db_name}'
        )
        self._engine = create_engine(
            connection_str,
            connect_args={'application_name': 'OSA transcription'},
        )
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self):
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def try_connection(self):
        try:
            connection = self._engine.connect()
            connection.close()
            return True
        except DatabaseError:
            return False
