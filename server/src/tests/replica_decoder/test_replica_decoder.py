import os
import subprocess
from unittest import TestCase

<<<<<<< HEAD
from connect_celery.database import PostworkDB
from decoder.decoder import postwork_decoder
from settings import (
    TEST_DB_HOST,
    TEST_DB_LOGIN,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
)


class ReplicaDecoderTest(TestCase):
    def setUp(self) -> None:
        self.db_dict = {
            'ip': TEST_DB_HOST,
            'port': TEST_DB_PORT,
            'db_login': TEST_DB_LOGIN,
            'db_password': TEST_DB_PASSWORD,
            'db_name': TEST_DB_NAME,
            'db_system': {'name': 'Postgres'},
        }
        self.database = PostworkDB(
            **self.db_dict,
        )
=======
from decoder.factory import DecoderFactory
from services.sprut import SprutService
from tests.base import BaseTest


class ReplicaDecoderTest(BaseTest, TestCase):
    def setUp(self) -> None:
        self.sprut_service = SprutService(self.db.session)
>>>>>>> e64f36e (server refactoring)

    def test_010_run_replica_decoder_without_args(self):
        action = 'replica_decoder/replica_decoder'
        process = subprocess.Popen(
            action,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid,
        )
        process.wait()
        out, err = process.communicate()
        self.assertEqual(process.returncode, 0)
        self.assertEqual(out.decode('utf-8'), 'invalid count parameters\n')

    def test_020_run_replica_decoder(self):
        record_id = 28
        self.sprut_service.mark_proc_record(record_id)
        raw_data = self.sprut_service.read_record_data_by_id(record_id)
        decoder = DecoderFactory().get_decoder(raw_data.codec)
        stream_f, stream_r = decoder.decode(
            raw_data.f_speech,
            raw_data.r_speech,
        )
        self.assertTrue(stream_f)
        self.assertFalse(stream_r)
