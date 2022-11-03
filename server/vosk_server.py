import asyncio
import io
import json
import websockets
import sys
import wave


class VoskServer:

    @staticmethod
    def _words_extract(response, percent) -> list:
        words = []
        try:
            response = json.loads(response)
            result = response['result']
            for word in result:
                if word['conf'] > percent:
                    words.append(word['word'])
            return words
        except Exception as e:
            return words

    @staticmethod
    def _text_extract(response) -> (list, str):
        conf = []
        try:
            response = json.loads(response)
            for word in response['result']:
                conf.append(word['conf'])
            return conf, response['text']
        except Exception as e:
            return [], ''

    def __init__(self, ip, port):
        self.connection_string = f'ws://{ip}:{port}'

    async def _keyword_recognize(self, speech_data, percent):
        words = []
        wav_stream = io.BytesIO(speech_data)
        async with websockets.connect(self.connection_string) as websocket:
            wav_signal = wave.open(wav_stream, 'rb')
            await websocket.send('{ "config" : { "sample_rate" : 16000, "words" : 1} }')
            buffer_size = 3200  # int(wf.getframerate() * 0.2) 0.2 seconds of audio
            while True:
                data = wav_signal.readframes(buffer_size)
                if len(data) == 0:
                    break
                await websocket.send(data)
                response = await websocket.recv()
                words += self._words_extract(response, percent)
            await websocket.send('{"eof" : 1}')
            response = await websocket.recv()
            words += self._words_extract(response, percent)
            return words

    async def _word_recognize(self, speech_data):
        conf = []
        text = ''
        con_int = 0
        wav_stream = io.BytesIO(speech_data)
        async with websockets.connect(self.connection_string) as websocket:
            wav_signal = wave.open(wav_stream, 'rb')
            await websocket.send('{ "config" : { "sample_rate" : 16000, "words" : 1 } }')
            buffer_size = 3200
            while True:
                data = wav_signal.readframes(buffer_size)
                if not data:
                    break
                await websocket.send(data)
                response = await websocket.recv()
                conf_partial, text_partial = self._text_extract(response)
                if text_partial:
                    conf = conf + conf_partial
                    text += f'{text_partial} '
            await websocket.send('{"eof" : 1}')
            response = await websocket.recv()
            conf_partial, text_partial = self._text_extract(response)
            if text_partial:
                conf = conf + conf_partial
                text += f'{text_partial} '
            if conf:
                for con in conf:
                    con_int += con
                con_int = con_int / len(conf)
                return con_int, text
            else:
                return con_int, text


    def recognize_chunk(self, data):
        if data:
            conf, text = asyncio.run(self._word_recognize(data))
            return conf, text
        else:
            return ''

    def recognize_keyword(self, data, percent):
        if data:
            words = asyncio.run(self._keyword_recognize(data, percent))
            return words
        else:
            return []


if __name__ == '__main__':
    vosk_server = VoskServer('localhost', 2700)
    with open('555.wav', 'rb') as file:
        byte_s = file.read()
    vosk_server.recognize_keyword(byte_s, 0.9)
