from unittest import TestCase
from settings import (
    TEST_DB_HOST,
    TEST_DB_LOGIN,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
    TEST_RU_VOSK_HOST,
    TEST_RU_VOSK_PORT,
    TEST_UA_VOSK_HOST,
    TEST_UA_VOSK_PORT,
)
from tests.base import BaseTest
from transcribing.processes.keyword_pr import KeywordIdentityProcess


class KeywordProcessTest(BaseTest, TestCase):
    def setUp(self) -> None:
        self.alias = 'logs\\123.log'
        self.db_dict = {
            'ip': TEST_DB_HOST,
            'port': TEST_DB_PORT,
            'db_login': TEST_DB_LOGIN,
            'db_password': TEST_DB_PASSWORD,
            'db_name': TEST_DB_NAME,
            'db_system': {'name': 'Postgres'},
        }
        self.models = [
            {
                'path': 'model-ru',
                'short_name': 'RU',
                'ip': TEST_RU_VOSK_HOST,
                'port': TEST_RU_VOSK_PORT,
            },
            {
                'path': 'model-ua',
                'short_name': 'UA',
                'ip': TEST_UA_VOSK_HOST,
                'port': TEST_UA_VOSK_PORT,
            },
        ]
        self.option_task = {
            'speech_time': 3,
            'keywords': 'привет\nхарьков\n^доброе$',
            'percent': 0.01,
        }

    def test_010_keyword_process(self):
        process = KeywordIdentityProcess('log')
        for model in self.models:
            process.setup_recognize_client(model['ip'], model['port'], model['short_name'])
        process.setup_database(
            self.db_dict['ip'],
            self.db_dict['port'],
            self.db_dict['db_login'],
            self.db_dict['db_password'],
            self.db_dict['db_name'],
            self.db_dict['db_system']['name'],
        )
        process.setup_options(
            self.option_task['speech_time'],
            self.option_task['percent'],
            self.option_task['keywords'].split('\n'),
        )
        process.handle_record(28)
