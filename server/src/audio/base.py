from io import BytesIO
from typing import List, NamedTuple, Tuple

from decoder.base import S16LE


class BaseVoiceError(Exception):
    message = ''

    def __init__(self, message=None, *args, **kwargs):
        if not message:
            super(BaseVoiceError, self).__init__(self.message, *args)
        else:
            super(BaseVoiceError, self).__init__(message, *args)


class WavBytesIO(BytesIO):
    ...


class VoiceChunks(NamedTuple):
    second_durations: int
    chunks: List[WavBytesIO]


class AbstractProvider:
    def get_durations(self, stream: S16LE) -> int:
        """return stream s16le durations in seconds"""
        raise NotImplementedError()

    def silence_split(self, stream: S16LE, *args, **kwargs) -> Tuple[int, List[BytesIO]]:
        """return non silens chunks and durations from s16le stream"""
        raise NotImplementedError()
