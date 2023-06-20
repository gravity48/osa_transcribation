from unittest import TestCase

from recognize_client.vosk import VoskClient
from settings import TEST_RU_VOSK_HOST, TEST_RU_VOSK_NAME, TEST_RU_VOSK_PORT
from tests.base import BaseTest
from words.words import KeywordsExtract


class TestWords(BaseTest, TestCase):
    def setUp(self) -> None:
        self.recognize_servers = [
            VoskClient(
                TEST_RU_VOSK_HOST,
                TEST_RU_VOSK_PORT,
                TEST_RU_VOSK_NAME,
            ),
        ]

    def test_010_empty_keywords(self):
        test_keywords = [self.fake.word() for _ in range(10)]
        extractor = KeywordsExtract(test_keywords)
        chunks_data = {item: self.fake.word() for item in range(10)}
        extractor.add_words_chunks(chunks_data)
        empty_str = extractor.get_format_text()
        self.assertFalse(empty_str)

    def test_020_true_find(self):
        test_keywords = [self.fake.unique.word() for _ in range(10)]
        extractor = KeywordsExtract(test_keywords)
        chunks_data = {
            item: [
                self.fake.unique.word(),
            ]
            for item in range(10)
        }
        chunks_data[0] = [
            test_keywords[0],
        ]
        extractor.add_words_chunks(chunks_data)
        result = extractor.get_format_text()
        self.assertTrue(result)

    def test_030_more_chunks(self):
        test_keywords = [self.fake.unique.word() for _ in range(10)]
        extractor = KeywordsExtract(test_keywords)
        chunks_data = {
            item: [
                self.fake.unique.word(),
            ]
            for item in range(10)
        }
        chunks_data[1] = [
            test_keywords[1],
        ]
        extractor.add_words_chunks(chunks_data)
        chunks_data = {
            item: [
                self.fake.unique.word(),
            ]
            for item in range(10)
        }
        chunks_data[2] = [test_keywords[2], test_keywords[4]]
        extractor.add_words_chunks(chunks_data)
        chunks_data = {
            item: [
                self.fake.unique.word(),
            ]
            for item in range(10)
        }
        chunks_data[3] = [
            test_keywords[3],
        ]
        extractor.add_words_chunks(chunks_data)
        result = extractor.get_format_text()
        result_list = result.split(' ')
        self.assertTrue(result)
        self.assertEqual(len(result_list), 4)

    def test_040_test_complicated_words(self):
        complicated_word = self.fake.word()

        test_keywords = [f'{complicated_word}', f'{self.fake.word()}']
        extractor = KeywordsExtract(test_keywords)
        chunks_data = {0: [f'234{complicated_word}123123', self.fake.unique.word()]}
        extractor.add_words_chunks(chunks_data)
        result = extractor.get_format_text()
        self.assertTrue(result)

    def test_041_test_complicated_words(self):
        complicated_word = self.fake.word()
        test_keywords = [
            f'{complicated_word}$',
        ]
        extractor = KeywordsExtract(test_keywords)
        chunks_data = {
            0: [
                f'fgdfg{complicated_word}',
            ],
        }
        extractor.add_words_chunks(chunks_data)
        result = extractor.get_format_text()
        self.assertTrue(result)
