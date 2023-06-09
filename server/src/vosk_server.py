import asyncio
import json
import websockets
import wave


class VoskServer:

    @staticmethod
    def _words_extract(response, percent) -> set:
        words = set()
        try:
            response = json.loads(response)
            result = response['result']
            for word in result:
                if word['conf'] > percent:
                    words.add(word['word'])
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

    async def _keyword_recognize(self, wav_signal: wave.Wave_read, percent, keywords):
        words = set()
        wav_signal.rewind()
        async with websockets.connect(self.connection_string) as websocket:
            conf = {
                'config': {
                    'sample_rate': wav_signal.getframerate(),
                    'words': 1
                }
            }
            await websocket.send(json.dumps(conf, ensure_ascii=False))
            buffer_size = int(wav_signal.getframerate() * 0.2)
            while True:
                data = wav_signal.readframes(buffer_size)
                if not len(data):
                    break
                await websocket.send(data)
                response = await websocket.recv()
                words.update(self._words_extract(response, percent))
            await websocket.send('{"eof" : 1}')
            response = await websocket.recv()
            words.update(self._words_extract(response, percent))
            return words

    async def _word_recognize(self, wav_signal: wave.Wave_read):
        conf = []
        text = ''
        con_int = 0
        wav_signal.rewind()
        async with websockets.connect(self.connection_string) as websocket:
            vosk_conf = {
                'config': {
                    'sample_rate': wav_signal.getframerate(),
                    'words': 1,
                }
            }
            await websocket.send(json.dumps(vosk_conf, ensure_ascii=False))
            buffer_size = int(wav_signal.getframerate() * 0.2)
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
                con_int = sum(conf)/len(conf)
                return con_int, text
            else:
                return con_int, text


    def recognize_chunk(self, wave_chunk):
        if wave_chunk:
            conf, text = asyncio.run(self._word_recognize(wave_chunk))
            return conf, text
        else:
            return ''

    def recognize_keyword(self, wave_chunk, percent, keywords):
        if wave_chunk:
            words = asyncio.run(self._keyword_recognize(wave_chunk, percent, keywords))
            return words
        else:
            return set()


if __name__ == '__main__':
    vosk_server = VoskServer('localhost', 2700)
    with open('555.wav', 'rb') as file:
        byte_s = file.read()
    vosk_server.recognize_keyword(byte_s, 0.9)
