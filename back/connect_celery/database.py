import fdb, copy, datetime #idb
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects import registry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import select
from sqlalchemy import Integer, Text, Column, TIMESTAMP, ForeignKey, Sequence, String, Time, VARCHAR, BLOB, DateTime, \
    SmallInteger
#from sqlalchemy.dialects.firebird.idb import FBDialect_idb

Base = declarative_base()

IB_LIB = '/opt/interbase/lib/libgds.so'
LIMIT_QUERY = 10

time_duration_max = datetime.time(0, 30, 0)
time_duration_min = datetime.time(0, 0, 5)


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


class SPR_SPEECH_TABLE(Base):
    __tablename__ = 'SPR_SPEECH_TABLE'
    s_type = Column(SmallInteger)
    s_inckey = Column(Integer, primary_key=True, autoincrement=True)
    s_datetime = Column(DateTime)
    s_standard = Column(VARCHAR(20))
    s_network = Column(VARCHAR(30))
    s_belong = Column(VARCHAR(30))
    s_calltype = Column(SmallInteger)
    s_sourceid = Column(Integer)
    s_sourcename = Column(VARCHAR(40))
    s_sysnumbertype = Column(VARCHAR(20))
    s_sysnumber = Column(VARCHAR(20))
    s_usernumber = Column(VARCHAR(40))
    s_usernumber_rev = Column(VARCHAR(40))
    s_priority = Column(Integer)
    s_talker = Column(VARCHAR(40))
    s_talker_rev = Column(VARCHAR(40))
    s_talkername = Column(VARCHAR(40))
    s_talkerid = Column(Integer)
    s_basestation = Column(VARCHAR(250))
    s_lac = Column(VARCHAR(30))
    s_cid = Column(VARCHAR(30))
    s_postid = Column(VARCHAR(20))
    s_deviceid = Column(VARCHAR(20))
    s_notice = Column(VARCHAR(100))
    s_prelooked = Column(SmallInteger)
    s_sysnumbertype2 = Column(VARCHAR(20))
    s_sysnumber2 = Column(VARCHAR(20))
    s_sysnumbertype3 = Column(VARCHAR(20))
    s_sysnumber3 = Column(VARCHAR(20))
    s_replicated = Column(SmallInteger)
    s_duration = Column(Time)
    s_selstatus = Column(SmallInteger)
    s_frequency = Column(VARCHAR(20))
    s_dchannel = Column(SmallInteger)
    s_rchannel = Column(SmallInteger)
    s_status = Column(SmallInteger)
    s_decryptinfo = Column(VARCHAR(10))
    s_event = Column(SmallInteger)
    s_postkey = Column(VARCHAR(64))
    s_eventcode = Column(VARCHAR(30))
    s_talker_bs = Column(VARCHAR(250))
    s_talker_lac = Column(VARCHAR(30))
    s_talker_cid = Column(VARCHAR(30))
    s_talker_sn = Column(VARCHAR(20))
    s_talker_sntype = Column(VARCHAR(20))
    s_talker_sn2 = Column(VARCHAR(20))
    s_talker_sntype2 = Column(VARCHAR(20))
    s_talker_sn3 = Column(VARCHAR(20))
    s_talker_sntype3 = Column(VARCHAR(20))


class SPR_EVENT(Base):
    __tablename__ = 'SPR_EVENT'
    val = Column(Integer, primary_key=True, autoincrement=True)
    val_name = Column(VARCHAR(50))

    def __init__(self, val_name):
        self.val_name = val_name


class SPR_SP_DATA_1_TABLE(Base):
    __tablename__ = 'SPR_SP_DATA_1_TABLE'
    s_inckey = Column(Integer, primary_key=True, autoincrement=True)
    s_order = Column(Integer)
    s_recordtype = Column(VARCHAR(30))
    s_fspeech = Column(BLOB)
    s_rspeech = Column(BLOB)
    s_spbookmark = Column(BLOB)
    s_spbookmarkrev = Column(BLOB)


class SPR_SP_COMMENT_TABLE(Base):
    __tablename__ = 'SPR_SP_COMMENT_TABLE'
    s_inckey = Column(Integer, primary_key=True)
    s_comment = Column(BLOB)

    def __init__(self, s_inckey, s_comment):
        self.s_inckey = s_inckey
        self.s_comment = s_comment


class PostworkDB:
    @open_session
    def read_data_from_id(self, s_inckey, session=None):
        data = session.query(SPR_SP_DATA_1_TABLE.s_fspeech, SPR_SP_DATA_1_TABLE.s_rspeech,
                             SPR_SP_DATA_1_TABLE.s_recordtype).filter(
            SPR_SP_DATA_1_TABLE.s_inckey == s_inckey).all()
        return data

    @open_session
    def add_comment_to_record(self, s_inckey, comment: str, session: Session = None):
        comment = comment.encode('cp1251')
        sp_comment_table: SPR_SP_COMMENT_TABLE = session.query(SPR_SP_COMMENT_TABLE).filter_by(s_inckey=s_inckey).all()
        if not sp_comment_table:
            session.add(SPR_SP_COMMENT_TABLE(s_inckey, comment))
        else:
            sp_comment_table[0].s_comment += comment
        session.commit()
        return True

    @open_session
    def mark_record(self, s_inckey, session: Session = None):
        session.query(SPR_SPEECH_TABLE).filter(SPR_SPEECH_TABLE.s_inckey == s_inckey).update({'s_decryptinfo': '+'})
        session.commit()
        pass

    @open_session
    def unmark_record(self, s_inckey, session: Session = None):
        session.query(SPR_SPEECH_TABLE).filter(SPR_SPEECH_TABLE.s_inckey == s_inckey).update({'s_decryptinfo': None})
        session.commit()
        pass

    @open_session
    def unmark_all_records(self, clean_comments=0, session: Session = None):
        session.query(SPR_SPEECH_TABLE).update({'s_decryptinfo': None})
        if clean_comments:
            sp_comment_tables = session.query(SPR_SP_COMMENT_TABLE).all()
            for sp_comment_table in sp_comment_tables:
                sp_comment_table.s_comment = ''.encode('cp1251')
        session.commit()
        pass

    def test_select(self):
        with self.session_master() as session:
            data = session.query(SPR_SP_DATA_1_TABLE).all()
        file = open('435.wav', 'wb')
        file.write(data[0].s_fspeech)
        file.close()
        print(data)

    def read_records_list(self, period_to, period_from, limit=None, offset=0):
        session = self.session_master()
        request_basis = session.query(SPR_SPEECH_TABLE.s_inckey).filter(SPR_SPEECH_TABLE.s_datetime >= period_from,
                                                                        SPR_SPEECH_TABLE.s_datetime <= period_to,
                                                                        SPR_SPEECH_TABLE.s_decryptinfo.is_(None),
                                                                        SPR_SPEECH_TABLE.s_eventcode == 'GSM',
                                                                        SPR_SPEECH_TABLE.s_duration <= time_duration_max,
                                                                        SPR_SPEECH_TABLE.s_duration >= time_duration_min).order_by(
            SPR_SPEECH_TABLE.s_datetime)
        records = request_basis.all()
        session.close()
        if limit:
            return records[offset:limit], len(records)
        else:
            return records, len(records)



    def try_connection(self):
        try:
            connection = self._engine.connect()
            connection.close()
            return True
        except DatabaseError:
            return False

    def connect(self):
        # (idb.fbcore.DatabaseError, fdb.fbcore.DatabaseError)
        if self._db_system == 'Interbase':
            connect = idb.connect(dsn=self._dsn, user=self._user, password=self._password, charset=self._charset,
                                  fb_library_name=IB_LIB)
        elif self._db_system == 'Firebird':
            connect = fdb.connect(dsn=self._dsn, user=self._user, password=self._password,
                                  charset=self._charset)
        self._is_connect = True
        return connect

    def __init__(self, server, port, login, password, db_name, db_system, charset='WIN1251'):
        registry.register("firebird.idb", "sqlalchemy.dialects.firebird.idb", "FBDialect_idb")
        connection_str = ''
        self._dsn = f'{server}/{port}:{db_name}'
        self._user = login
        self._password = password
        self._charset = charset
        self._db_system = db_system
        self._is_connect = False
        if db_system == 'Interbase':
            connection_str = f'firebird+idb://{login}:{password}@{server}:{port}/{db_name}?' \
                             f'fb_library_name={IB_LIB}&charset={charset}'

        elif db_system == 'Firebird':
            connection_str = f'firebird+fdb://{login}:{password}@{server}:{port}/{db_name}?&charset={charset}'
        self._engine = create_engine(connection_str)
        self.session_master = sessionmaker(bind=self._engine)
        self.cursor = None


if __name__ == '__main__':
    serv = '172.16.71.133'
    port = '3050'
    user = 'SYSDBA'
    password = 'masterkey'
    db_name = 'c:\\databases\\TEMP_GSM.IBS'
