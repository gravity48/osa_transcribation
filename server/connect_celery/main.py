import idb
import fdb
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects import registry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Text, Column, ForeignKey, Sequence, String, VARCHAR
from sqlalchemy.dialects.firebird.idb import FBDialect_idb
from connect_celery.database import PostworkDB

IB_LIB = '/lib/i386-linux-gnu/libgds.so'


def connect2database(server, port, login, password, db_name, db_system, charset='WIN1251'):
    postwork_db = PostworkDB(server, port, login, password, db_name, db_system, charset)
    status = postwork_db.try_connection()
    postwork_db.test_select()
    return status


if __name__ == '__main__':
    postwork_db = PostworkDB('172.16.71.131', '3050', 'sysdba', 'masterkey', 'c:\\Databases\\123.ibs', 'INTERBASE',
                             'WIN1251')

    status = postwork_db.try_connection()
    postwork_db.test_select()
