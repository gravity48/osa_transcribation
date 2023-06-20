from typing import Dict, List

from recognize_client.base import RecognizeOutput


class AbstractExtract:
    def add_words_chunks(self, chunks_data: Dict[int, List[str]]) -> None:
        raise NotImplementedError

    def add_duplex_words_chunks(
        self,
        words_f: RecognizeOutput,
        words_r: RecognizeOutput,
        name: str,
    ) -> None:
        raise NotImplementedError

    def get_format_text(self):
        raise NotImplementedError


class BaseExtract(AbstractExtract):
    def add_words_chunks(self, chunks_data: Dict[int, List[str]]) -> None:
        raise NotImplementedError

    def add_duplex_words_chunks(
        self,
        words_f: RecognizeOutput,
        words_r: RecognizeOutput,
        name: str,
    ) -> None:
        self.add_words_chunks(words_f.chunks_data)
        self.add_words_chunks(words_r.chunks_data)

    def get_format_text(self):
        raise NotImplementedError
