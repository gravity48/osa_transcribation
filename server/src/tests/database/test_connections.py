from datetime import datetime
from unittest import TestCase

<<<<<<< HEAD
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
=======
from services.sprut import SprutService
from tests.base import BaseTest


class DatabaseTest(BaseTest, TestCase):
    def setUp(self) -> None:
        self.service = SprutService(self.db.session)
>>>>>>> e64f36e (server refactoring)

    def test_010_connection(self):
        self.assertTrue(self.db.try_connection())

<<<<<<< HEAD
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
=======
    def test_030_get_record_data(self):
        data = self.service.read_record_data_by_id(30)
        self.assertEqual(data.codec, 'GSM')

    def test_040_mark_record(self):
        self.service.mark_proc_record(30)
        sst_row = self.test_service.get_data_from_sst_by_id(30)
        self.assertEqual(sst_row['s_decryptinfo'], '+')

    def test_050_update_notice_text(self):
        self.service.update_notice_text(28, 'some_text')
        self.service.update_notice_text(28, 'some_text')
        result = self.test_service.get_data_from_sst_by_id(28)
        self.assertEqual(result['s_notice'], ' keyword: some_text keyword: some_text')

    def test_060_read_record_list(self):
        result = self.service.select_records(
            datetime.strptime('01-09-2022', '%d-%m-%Y'),
            datetime.strptime('30-10-2022', '%d-%m-%Y'),
        )
        self.assertEqual(len(result), 385)

        result = self.service.select_records(
            datetime.strptime('01-09-2022', '%d-%m-%Y'),
            datetime.strptime('30-10-2022', '%d-%m-%Y'),
            post='MANGO',
        )
        self.assertEqual(len(result), 4)

        result = self.service.select_records(
            datetime.strptime('01-09-2022', '%d-%m-%Y'),
            datetime.strptime('30-10-2022', '%d-%m-%Y'),
            limit=100,
        )
        self.assertEqual(len(result), 100)

        result = self.service.select_records(
            datetime.strptime('30-09-2023', '%d-%m-%Y'),
            datetime.strptime('30-10-2025', '%d-%m-%Y'),
            limit=100,
        )
        self.assertFalse(result)
>>>>>>> e64f36e (server refactoring)
