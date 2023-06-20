from datetime import datetime
from typing import List

from database_sprut.models import SprSpData1Table, SprSpeechTable
from database_sprut.structs import RowData
from decoder.factory import DecoderFactory
from settings import MAX_DURATION, MIN_DURATION
from sqlalchemy import select, update
from sqlalchemy.sql.functions import concat


class SprutService:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def read_record_data_by_id(self, s_inckey: int) -> RowData:
        with self._session_factory() as session:
            query = select(
                SprSpData1Table.s_fspeech,
                SprSpData1Table.s_rspeech,
                SprSpData1Table.s_recordtype,
            ).where(
                SprSpData1Table.s_inckey == s_inckey,
            )
            result = session.execute(query).one()
            row_data = RowData(result.s_fspeech, result.s_rspeech, result.s_recordtype)
        return row_data

    def mark_proc_record(self, s_inckey: int):
        with self._session_factory() as session:
            query = (
                update(SprSpeechTable)
                .where(SprSpeechTable.s_inckey == s_inckey)
                .values(s_decryptinfo='+')
            )
            session.execute(query)

    def mark_pre_proc_record(self, s_inckey: int):
        with self._session_factory() as session:
            query = (
                update(SprSpeechTable)
                .where(SprSpeechTable.s_inckey == s_inckey)
                .values(s_decryptinfo='queue')
            )
            session.execute(query)

    def update_notice_text(self, s_inckey, text):
        if not text:
            return
        text = f' keyword: {text}'
        with self._session_factory() as session:
            query = (
                update(SprSpeechTable)
                .where(SprSpeechTable.s_inckey == s_inckey)
                .values(s_notice=concat(SprSpeechTable.s_notice, text))
            )
            session.execute(query)
            session.commit()

    def select_records(
        self,
        period_from: datetime,
        period_to: datetime,
        post: str = '',
        selection: bool = False,
        limit: int = None,
        offset: int = 0,
    ) -> List[int]:
        query = (
            select(SprSpeechTable.s_inckey)
            .join(SprSpData1Table, SprSpData1Table.s_inckey == SprSpeechTable.s_inckey)
            .where(
                SprSpeechTable.s_datetime >= period_from,
                SprSpeechTable.s_datetime <= period_to,
                SprSpeechTable.s_decryptinfo.is_(None),
                SprSpeechTable.s_duration <= MAX_DURATION,
                SprSpeechTable.s_duration >= MIN_DURATION,
                SprSpData1Table.s_recordtype.in_(DecoderFactory.decoders.keys()),
            )
        )
        if post:
            query = query.where(SprSpeechTable.s_postid == post)
        if selection:
            query = query.where(
                SprSpeechTable.s_talkername.is_(None),
                SprSpeechTable.s_sourcename.is_(None),
            )
        if limit:
            query = query.limit(limit).offset(offset)
        with self._session_factory() as session:
            query = query.order_by(SprSpeechTable.s_datetime.desc())
            results = session.execute(query).all()
            return [r for r, in results]
