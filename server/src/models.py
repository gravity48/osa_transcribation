import io
import json
import re
import wave

import numpy as np
from vosk import KaldiRecognizer, Model, SpkModel


class TranscribingModel:
    @staticmethod
    def clean_text(text):
        text_clear = re.sub(r'[\s|\n]', '', text)
        return text_clear

    @staticmethod
    def cosine_dist(x, y):
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    def text_from_wav(self, filename):
        wav_text = ''
        wav_signal = wave.open(filename, 'rb')
        if (
            wav_signal.getnchannels() != 1
            or wav_signal.getsampwidth() != 2
            or wav_signal.getcomptype() != "NONE"
        ):
            print("Audio file must be WAV format mono PCM.")
        while True:
            data = wav_signal.readframes(4000)
            # data = wav_signal.readframes(wav_signal.getnframes())
            if not data:
                break
            if self.recognizer.AcceptWaveform(data):
                wav_text += ' ' + json.loads(self.recognizer.Result())['text']
            else:
                try:
                    wav_text += ' ' + json.loads(self.recognizer.PartialResult())['text']
                except KeyError:
                    wav_text += ''
        return wav_text

    def __init__(self, model_name):
        self.model_name = model_name
        self.recognizer = None

    def set_spk_models(self, spk_model_path):
        spk_model = SpkModel(spk_model_path)
        self.recognizer.SetSpkModel(spk_model)

    def get_speaker_vector(self, filepath):
        wav_signal = wave.open(filepath, 'rb')
        data = wav_signal.readframes(wav_signal.getnframes())
        if (
            wav_signal.getnchannels() != 1
            or wav_signal.getsampwidth() != 2
            or wav_signal.getcomptype() != "NONE"
        ):
            print("Audio file must be WAV format mono PCM.")
        self.recognizer.AcceptWaveform(data)
        result = json.loads(self.recognizer.FinalResult())
        return result['spk']

    def get_vectors_from_data(self, data, spk_vector):
        r_vector = None
        f_vector = None
        f_speech, r_speech = data
        if r_speech != b'':
            r_vector = self._vector_from_binary(r_speech)
        if f_speech != b'':
            f_vector = self._vector_from_binary(f_speech)
        del data
        return r_vector, f_vector

    def train(self):
        model = Model(self.model_name)
        self.recognizer = KaldiRecognizer(model, 16000)

    def _wav_to_text(self, speech_data):
        wav_stream = io.BytesIO(speech_data)
        wav_signal = wave.open(wav_stream, 'rb')
        if (
            wav_signal.getnchannels() != 1
            or wav_signal.getsampwidth() != 2
            or wav_signal.getcomptype() != "NONE"
        ):
            print("Audio file must be WAV format mono PCM.")
        while True:
            data = wav_signal.readframes(4000)
            # data = wav_signal.readframes(wav_signal.getnframes())
            if not data:
                break
            self.recognizer.AcceptWaveform(data)
        wav_text = json.loads(self.recognizer.FinalResult())['text']
        return wav_text

    def _word_recognize(self, speech_data):
        self.recognizer.SetWords(True)
        self.recognizer.SetPartialWords(True)
        wav_stream = io.BytesIO(speech_data)
        wav_signal = wave.open(wav_stream, 'rb')
        while True:
            data = wav_signal.readframes(4000)
            if not data:
                break
            self.recognizer.AcceptWaveform(data)
        result_json = json.loads(self.recognizer.FinalResult())
        conf = 0
        try:
            for word in result_json['result']:
                conf += word['conf']
            conf = conf / len(result_json['result'])
            return conf, result_json['text']
        except Exception as e:
            return 0, result_json['text']

    def _keyword_recognize(self, speech_data, percent):
        words = []
        self.recognizer.SetWords(True)
        self.recognizer.SetPartialWords(True)
        wav_stream = io.BytesIO(speech_data)
        wav_signal = wave.open(wav_stream, 'rb')
        while True:
            data = wav_signal.readframes(4000)
            if not data:
                break
            self.recognizer.AcceptWaveform(data)
        result_json = json.loads(self.recognizer.FinalResult())
        try:
            for word in result_json['result']:
                if word['conf'] > percent:
                    words.append(word['word'])
            return words
        except Exception as e:
            return words

    def _vector_from_binary(self, speech_data):
        wav_stream = io.BytesIO(speech_data)
        wav_signal = wave.open(wav_stream, 'rb')
        while True:
            # data = wav_signal.readframes(4000)
            data = wav_signal.readframes(wav_signal.getnframes())
            if not data:
                break
            self.recognizer.AcceptWaveform(data)
        result = json.loads(self.recognizer.FinalResult())
        return result['spk']

    def recognize(self, data):
        r_text = ''
        f_text = ''
        f_speech, r_speech = data
        if r_speech != b'':
            r_text += self._wav_to_text(r_speech)
        if f_speech != b'':
            f_text += self._wav_to_text(f_speech)
        del data
        return f_text, r_text

    def recognize_chunk(self, data):
        if data:
            conf, text = self._word_recognize(data)
            return conf, text
        else:
            return ''

    def recognize_keyword(self, data, percent):
        if data:
            words = self._keyword_recognize(data, percent)
            return words
        else:
            return []
