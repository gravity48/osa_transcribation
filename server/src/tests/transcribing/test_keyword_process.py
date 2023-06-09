import os
from multiprocessing import Queue, Value
from unittest import TestCase

from loguru import logger

from connect_celery.database import PostworkDB
from settings import TEST_DB_HOST, TEST_DB_PORT, TEST_DB_LOGIN, TEST_DB_PASSWORD, TEST_DB_NAME, TEST_RU_VOSK_HOST, \
    TEST_RU_VOSK_PORT, TEST_UA_VOSK_HOST, TEST_UA_VOSK_PORT
from transcribing.keyword_pr import keyword_identification_process


class KeywordProcessTest(TestCase):

    def setUp(self) -> None:
        self.alias = 'logs\\123.log'
        self.db_dict = {
            'ip': TEST_DB_HOST,
            'port': TEST_DB_PORT,
            'db_login': TEST_DB_LOGIN,
            'db_password': TEST_DB_PASSWORD,
            'db_name': TEST_DB_NAME,
            'db_system': {
                'name': 'Postgres'
            }
        }
        self.database = PostworkDB(
            **self.db_dict,
        )
        self.models = [
            {
                'path': 'model-ru',
                'short_name': 'RU',
                'ip': TEST_RU_VOSK_HOST,
                'port': TEST_RU_VOSK_PORT
            },

            {
                'path': 'model-ua',
                'short_name': 'UA',
                'ip': TEST_UA_VOSK_HOST,
                'port': TEST_UA_VOSK_PORT
            }
        ]
        option_task = {
            'speech_time': 3,
            'keywords': 'привет\nхарьков\n^доброе$',
        }
        option_connections = {

        }
        self.keywords = option_task['keywords'].split('\n')
        logger.add(
            self.alias,
            filter=lambda record: self.alias in record["extra"],
            format="{time} {level} {message}",
            level="INFO"
        )

    def tearDown(self):
        self.database.unmark_all_records(True)

    def test_010_keyword_identification_process(self):
        queue = Queue()
        queue.put(28)
        is_run = Value('i', 1)
        records_processed = Value('i', 0)
        keyword_identification_process(
            queue,
            is_run,
            self.db_dict,
            self.models,
            {self.alias: True},
            1,
            records_processed,
            2,
            self.keywords,
            0.01,
            debug=True,
        )
