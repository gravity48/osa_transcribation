from typing import NamedTuple

from database_sprut.base import SpeechBlob


class RowData(NamedTuple):
    f_speech: SpeechBlob
    r_speech: SpeechBlob
    codec: str
