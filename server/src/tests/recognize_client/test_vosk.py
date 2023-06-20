from unittest import TestCase

from audio.audio import AudioHandler
from decoder.factory import DecoderFactory
from recognize_client.vosk import VoskClient
from services.sprut import SprutService
from settings import (
    TEST_RU_VOSK_HOST,
    TEST_RU_VOSK_NAME,
    TEST_RU_VOSK_PORT,
    TEST_UA_VOSK_HOST,
    TEST_UA_VOSK_NAME,
    TEST_UA_VOSK_PORT,
)
from tests.base import BaseTest


class TestVoskClient(BaseTest, TestCase):
    def setUp(self) -> None:
        self.vosk_client = VoskClient(
            TEST_RU_VOSK_HOST,
            TEST_RU_VOSK_PORT,
            TEST_RU_VOSK_NAME,
        )
        self.vosk_servers = [
            self.vosk_client,
            VoskClient(TEST_UA_VOSK_HOST, TEST_UA_VOSK_PORT, TEST_UA_VOSK_NAME),
        ]

    def test_010_connection(self):
        status = self.vosk_client.connect()
        self.assertTrue(status)

    def test_015_non_existent_connection(self):
        non_exists_vosk_client = VoskClient(
            TEST_RU_VOSK_HOST,
            8888,
            TEST_RU_VOSK_NAME,
        )
        status = non_exists_vosk_client.connect()
        self.assertFalse(status)

    def test_020_get_words_bad_response(self):
        response = b'{"1231":"123"}'
        result = self.vosk_client._get_words(response, 0.1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_030_recognize_chunks(self):
        record_id = 28
        sprut_service = SprutService(self.db.session)
        row_data = sprut_service.read_record_data_by_id(record_id)
        decoder = DecoderFactory().get_decoder(row_data.codec)
        stream_f, stream_r = decoder.decode(
            row_data.f_speech,
            row_data.r_speech,
        )
        audio_handler = AudioHandler(stream_f, stream_r)
        audio_handler.split_silence()
        chunks_f, chunks_r = audio_handler.chunks
        words_f, words_r = self.vosk_client.recognize_duplex(chunks_f, chunks_r, 0.01)
        self.assertTrue(words_f.count > 0)
        self.assertEqual(words_r.count, 0)

    def test_040_multiply_servers(self):
        record_id = 42
        sprut_service = SprutService(self.db.session)
        row_data = sprut_service.read_record_data_by_id(record_id)
        decoder = DecoderFactory().get_decoder(row_data.codec)
        stream_f, stream_r = decoder.decode(
            row_data.f_speech,
            row_data.r_speech,
        )
        audio_handler = AudioHandler(stream_f, stream_r)
        audio_handler.split_silence()
        chunks_f, chunks_r = audio_handler.chunks
        for client in self.vosk_servers:
            words_f, words_r = client.recognize_duplex(chunks_f, chunks_r, 0.01)
            self.assertTrue(words_f.count > 0)
            self.assertEqual(words_r.count, 0)
