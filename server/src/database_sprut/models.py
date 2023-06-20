from database_sprut.db.postgres import Base
from sqlalchemy import BLOB, VARCHAR, Column, DateTime, Integer, SmallInteger, Time

from .base import BaseModels


class SprSpeechTable(BaseModels, Base):
    __tablename__ = 'spr_speech_table'
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


class SprEvent(Base):
    __tablename__ = 'spr_event'
    val = Column(Integer, primary_key=True, autoincrement=True)
    val_name = Column(VARCHAR(50))

    def __init__(self, val_name):
        self.val_name = val_name


class SprSpData1Table(Base):
    __tablename__ = 'spr_sp_data_1_table'
    s_inckey = Column(Integer, primary_key=True, autoincrement=True)
    s_order = Column(Integer)
    s_recordtype = Column(VARCHAR(30))
    s_fspeech = Column(BLOB)
    s_rspeech = Column(BLOB)
    s_spbookmark = Column(BLOB)
    s_spbookmarkrev = Column(BLOB)


class SprSpCommentTable(Base):
    __tablename__ = 'spr_sp_comment_table'
    s_inckey = Column(Integer, primary_key=True)
    s_comment = Column(BLOB)

    def __init__(self, s_inckey, s_comment):
        self.s_inckey = s_inckey
        self.s_comment = s_comment
