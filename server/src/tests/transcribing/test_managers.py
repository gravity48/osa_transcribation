import time
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
from transcribing.taks.keyword_task import KeywordTask


class TestKeywordManagers(BaseTest, TestCase):
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
        self.filter = {'period_from': '2020-06-19T18:09:12Z', 'period_to': '2023-06-19T18:09:12Z'}
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
        self.ctl_options = {
            'selection': False,
            'post': '',
        }
        self.worker_options = {
            'speech_time': 3,
            'keywords': 'привет\nхарьков\n^доброе$',
            'percent': 0.01,
        }

    def test_010_run_keywords(self):
        task = KeywordTask(self.alias, 4)
        task.setup_db_options(
            self.db_dict['ip'],
            self.db_dict['port'],
            self.db_dict['db_login'],
            self.db_dict['db_password'],
            self.db_dict['db_name'],
            self.db_dict['db_system']['name'],
        )
        task.setup_filter(**self.filter)
        task.setup_ctl_options(**self.ctl_options)
        task.setup_worker_options(**self.worker_options)
        for model in self.models:
            task.setup_recognize_client(model['ip'], model['port'], model['short_name'])
        task.start()
        for _ in range(10):
            time.sleep(10)
            print(task.status())
        task.stop()
        for _ in range(10):
            time.sleep(2)
