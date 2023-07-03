from datetime import datetime
from unittest import TestCase

from connect_celery.database import PostworkDB
from settings import (
    TEST_DB_HOST,
    TEST_DB_LOGIN,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
)


class DatabaseTest(TestCase):
    def setUp(self):
        self.host = TEST_DB_HOST
        self.port = TEST_DB_PORT
        self.db_name = TEST_DB_NAME
        self.login = TEST_DB_LOGIN
        self.password = TEST_DB_PASSWORD
        self.service = PostworkDB(
            self.host,
            self.port,
            self.login,
            self.password,
            self.db_name,
            {'name': 'Postgres'},
        )

    def test_010_connection(self):
        self.assertTrue(self.service.try_connection())

    def test_020_filter_100_records(self):
        period_from = datetime.strptime('01-09-2022', '%d-%m-%Y')
        period_to = datetime.strptime('30-10-2022', '%d-%m-%Y')
        data, record_count = self.service.read_records_list(
            period_to,
            period_from,
            {'post': 'POROZ'},
            100,
            0,
        )
        self.assertEqual(len(data), 100)
