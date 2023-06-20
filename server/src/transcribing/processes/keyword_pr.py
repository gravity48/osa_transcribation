from typing import Dict, List

from audio.audio import AudioHandler
from decoder.factory import DecoderFactory
from recognize_client.base import AbstractRecognizeClient
from recognize_client.vosk import VoskClient
from transcribing.base import InfinityProcess
from transcribing.exceptions import ContinueProcessError
from transcribing.mixins import SetupSprutMixin
from words.base import AbstractExtract
from words.words import KeywordsExtract


class KeywordIdentityProcess(SetupSprutMixin, InfinityProcess):
    recognize_servers: List[AbstractRecognizeClient]
    options: Dict
    extractor: AbstractExtract

    def setup_recognize_client(self, host: str, port: int, name: str):
        if not hasattr(self, 'recognize_servers'):
            self.recognize_servers = []
        self.recognize_servers.append(VoskClient(host=host, port=port, name=name))

    def setup_options(self, speech_time: int, percent: float, keywords: List[str]):
        self.options = dict()
        self.options['speech_time'] = speech_time
        self.options['percent'] = percent
        self.extractor = KeywordsExtract(keywords)

    def handle_record(self, record_id: int) -> None:
        self.sprut_service.mark_proc_record(record_id)
        row_data = self.sprut_service.read_record_data_by_id(record_id)
        decoder = DecoderFactory().get_decoder(row_data.codec)
        stream_f, stream_r = decoder.decode(
            row_data.f_speech,
            row_data.r_speech,
        )
        audio_handler = AudioHandler(stream_f, stream_r)
        audio_handler.split_silence()
        if audio_handler.check_empty(self.options['speech_time']):
            self.sprut_service.mark_proc_record(record_id)
            raise ContinueProcessError()
        chunks_f, chunks_r = audio_handler.chunks
        for client in self.recognize_servers:
            words_f, words_r = client.recognize_duplex(
                chunks_f=chunks_f,
                chunks_r=chunks_r,
                percent=self.options.get('percent', 0),
            )
            self.extractor.add_duplex_words_chunks(
                words_f,
                words_r,
                client.name,
            )
        self.sprut_service.update_notice_text(record_id, self.extractor.get_format_text())
