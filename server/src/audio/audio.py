from typing import List, Tuple

from decoder.base import S16LE

from .base import WavBytesIO
from .exceptions import InvalidOperation
from .providers import PydubProvider


class AudioHandler:
    provider = PydubProvider()

    def __init__(self, stream_f: S16LE, stream_r: S16LE):
        self._stream_f = stream_f
        self._stream_r = stream_r
        self._chunks_f = None
        self._chunks_r = None
        self._dur_f = None
        self._dur_r = None

    @property
    def raw_durations(self) -> Tuple[int, int]:
        """return durations raw data in seconds"""
        f_durations = self.provider.get_durations(self._stream_f)
        r_durations = self.provider.get_durations(self._stream_r)
        return f_durations, r_durations

    @property
    def chunk_durations(self) -> Tuple[int, int]:
        if self._dur_f is None or self._dur_r is None:
            raise InvalidOperation()
        return self._dur_f, self._dur_r

    @property
    def chunks(self) -> Tuple[List[WavBytesIO], List[WavBytesIO]]:
        if self._chunks_f is None or self._chunks_r is None:
            raise InvalidOperation()
        return self._chunks_f, self._chunks_r

    def check_empty(self, speech_time: int) -> bool:
        if self._dur_f is None or self._dur_r is None:
            raise InvalidOperation()
        return self._dur_f < speech_time and self._dur_r < speech_time

    def split_silence(self) -> None:
        self._dur_f, self._chunks_f = self.provider.silence_split(self._stream_f, normalize=True)
        self._dur_r, self._chunks_r = self.provider.silence_split(self._stream_r, normalize=True)
        return
