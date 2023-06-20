from typing import List, Tuple

from audio.base import WavBytesIO


class RecognizeOutput:
    def __init__(self, name: str):
        self.name = name
        self.chunks_data = {}

    @property
    def count(self):
        return len(self.chunks_data)


class AbstractRecognizeClient:
    name: str

    def connect(self) -> bool:
        raise NotImplementedError

    def recognize_words(self, chunks: List[WavBytesIO], percent: float = 0) -> RecognizeOutput:
        raise NotImplementedError

    def recognize_duplex(
        self,
        chunks_f: List[WavBytesIO],
        chunks_r: List[WavBytesIO],
        percent: float = 0,
    ) -> Tuple[RecognizeOutput, RecognizeOutput]:
        raise NotImplementedError


class BaseRecognizeClient(AbstractRecognizeClient):
    def connect(self) -> bool:
        raise NotImplementedError

    def recognize_words(self, chunks: List[WavBytesIO], percent: float = 0) -> RecognizeOutput:
        raise NotImplementedError

    def recognize_duplex(
        self,
        chunks_f: List[WavBytesIO],
        chunks_r: List[WavBytesIO],
        percent: float = 0,
    ):
        words_f = self.recognize_words(chunks_f, percent)
        words_r = self.recognize_words(chunks_r, percent)
        return words_f, words_r
