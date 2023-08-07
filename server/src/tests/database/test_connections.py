from datetime import datetime
from unittest import TestCase
from services.sprut import SprutService
from tests.base import BaseTest


class DatabaseTest(BaseTest, TestCase):
    def setUp(self) -> None:
        self.service = SprutService(self.db.session)

    def test_010_connection(self):
        self.assertTrue(self.db.try_connection())

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
