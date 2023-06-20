from datetime import datetime
from multiprocessing import Queue
from unittest import TestCase

from settings import (
    TEST_DB_HOST,
    TEST_DB_LOGIN,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
)
from tests.base import BaseTest
from transcribing.processes.control_pr import ControlProcess


class ControlTest(BaseTest, TestCase):
    def test_010_control_handler(self):
        process = ControlProcess('test')
        process.setup_database(
            host=TEST_DB_HOST,
            port=TEST_DB_PORT,
            login=TEST_DB_LOGIN,
            password=TEST_DB_PASSWORD,
            path=TEST_DB_NAME,
            provider_name='Postgres',
        )
        process.setup_period(
            period_from=datetime.strptime('2020-06-19T18:09:12Z', '%Y-%m-%dT%H:%M:%S%z'),
            period_to=datetime.strptime('2023-06-19T18:09:12Z', '%Y-%m-%dT%H:%M:%S%z'),
        )
        process.setup_options()
        queue = Queue(10)
        process.control_handler(queue)
