import json
import wave
from json import JSONDecodeError
from typing import List

from audio.base import WavBytesIO
from recognize_client.base import BaseRecognizeClient, RecognizeOutput
from websockets.sync.client import connect


class VoskClient(BaseRecognizeClient):
    voice_interval = 0.2

    def __init__(self, host, port, name):
        self.dsn_ = f'ws://{host}:{port}'
        self.name = name

    def connect(self) -> bool:
        try:
            with connect(self.dsn_):
                return True
        except ConnectionRefusedError:
            return False

    @staticmethod
    def _get_words(response: bytes, percent: float) -> List[str]:
        words_ = []
        try:
            response = json.loads(response)
            items = response['result']
            for item in items:
                if item['conf'] > percent:
                    words_.append(item['word'])
            return words_
        except (TypeError, KeyError, JSONDecodeError):
            return words_

    def recognize_chunk_words(self, chunk: WavBytesIO, percent) -> List[str]:
        words = []
        chunk.seek(0)
        voice = wave.open(chunk, 'rb')
        with connect(self.dsn_) as client:
            conf = {'config': {'sample_rate': voice.getframerate(), 'words': 1}}
            client.send(json.dumps(conf, ensure_ascii=False))
            buffer_size = int(voice.getframerate() * self.voice_interval)
            while True:
                data = voice.readframes(buffer_size)
                if not len(data):
                    break
                client.send(data)
                response = client.recv()
                words += self._get_words(response, percent)
            client.send('{"eof" : 1}')
            response = client.recv()
            words += self._get_words(response, percent)
            voice.close()
            return words

    def recognize_words(self, chunks: List[WavBytesIO], percent: float = 0) -> RecognizeOutput:
        if not chunks:
            return RecognizeOutput(self.name)
        output = RecognizeOutput(self.name)
        for item, chunk in enumerate(chunks):
            output.chunks_data[item] = self.recognize_chunk_words(chunk, percent)
        return output
