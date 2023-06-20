from database_sprut.db.postgres import PostgresSprutDatabase
from faker import Faker
from services.tests import TestSprutService
from settings import (
    TEST_DB_HOST,
    TEST_DB_LOGIN,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
)


class BaseTest:
    @classmethod
    def setUpClass(cls):
        cls.db = PostgresSprutDatabase(
            ip=TEST_DB_HOST,
            port=TEST_DB_PORT,
            db_login=TEST_DB_LOGIN,
            db_password=TEST_DB_PASSWORD,
            db_name=TEST_DB_NAME,
        )

        cls.test_service = TestSprutService(cls.db.session)
        cls.fake = Faker(['ru_RU'])

    def tearDown(self):
        self.test_service.unmark_all_records(clean_comments=False)
