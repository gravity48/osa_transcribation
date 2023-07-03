from functools import wraps

from sqlalchemy import (
    BLOB,
    TIMESTAMP,
    VARCHAR,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    SmallInteger,
    String,
    Text,
    Time,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()


def open_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_master = sessionmaker(bind=args[0]._engine)
        session = session_master()
        kwargs['session'] = session
        result = func(*args, **kwargs)
        session.close()
        return result

    return wrapper


class TASKS(Base):
    __tablename__ = 'tasks_tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    percent = Column(Integer)
    processed_record_id = Column(Integer)
    record_count = Column(Integer)
    force_stop = Column(Boolean)


class SettingsDB:
    def __init__(self, login, password, host, db_name):
        connection_str = f'postgresql+psycopg2://{login}:{password}@{host}/{db_name}'
        self._engine = create_engine(connection_str)
        self.session_master = sessionmaker(bind=self._engine)

    @open_session
    def write_percent(self, record_id, percent, processed_record_id, session: Session = None):
        session.query(TASKS).filter_by(id=record_id).update(
            {'percent': percent, 'processed_record_id': processed_record_id},
        )
        session.commit()
        pass

    @open_session
    def write_record_count(self, record_id, record_count, session: Session = None):
        session.query(TASKS).filter_by(id=record_id).update({'record_count': record_count})
        session.commit()
        pass

    @open_session
    def get_force_stop(self, record_id, session: Session = None):
        force_stop = session.query(TASKS.force_stop).filter_by(id=record_id).all()[0][0]
        return force_stop
