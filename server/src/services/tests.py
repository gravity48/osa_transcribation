from database_sprut.models import SprSpCommentTable, SprSpeechTable
from sqlalchemy import update


class TestSprutService:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    def unmark_all_records(self, clean_comments: bool = False):
        with self._session_factory() as session:
            query = (
                update(SprSpeechTable)
                .where(SprSpeechTable.s_inckey > 0)
                .values(s_notice=None, s_decryptinfo=None)
            )
            session.execute(query)
            if clean_comments:
                query = (
                    update(SprSpCommentTable)
                    .where(SprSpCommentTable > 0)
                    .values(s_comment=''.encode('UTF8'))
                )
                session.execute(query)

    def get_data_from_sst_by_id(self, s_inckey: int):
        with self._session_factory() as session:
            result = session.query(SprSpeechTable).filter(SprSpeechTable.s_inckey == s_inckey).one()
            return result.as_dict()
