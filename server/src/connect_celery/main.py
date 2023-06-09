import fdb
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects import registry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Text, Column, ForeignKey, Sequence, String, VARCHAR
from connect_celery.database import PostworkDB


def connect2database(server, port, login, password, db_name, db_system, charset='WIN1251'):
    postwork_db = PostworkDB(server, port, login, password, db_name, db_system, charset)
    status = postwork_db.try_connection()
    postwork_db.test_select()
    return status



