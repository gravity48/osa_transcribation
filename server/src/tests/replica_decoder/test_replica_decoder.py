import os
import subprocess
from unittest import TestCase

from connect_celery.database import PostworkDB
from decoder.decoder import postwork_decoder
from settings import TEST_DB_HOST, TEST_DB_PORT, TEST_DB_LOGIN, TEST_DB_PASSWORD, TEST_DB_NAME


class ReplicaDecoderTest(TestCase):

    def setUp(self) -> None:
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

    def test_010_run_replica_decoder_without_args(self):
        action = f'replica_decoder/replica_decoder'
        process = subprocess.Popen(
            action,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        process.wait()
        out, err = process.communicate()
        self.assertEqual(process.returncode, 0)
        self.assertEqual(out.decode("utf-8"), 'invalid count parameters\n')

    def test_020_run_replica_decoder(self):
        record_id = 28
        self.database.mark_record(record_id)
        data = self.database.read_data_from_id(record_id)
        speech_decode = postwork_decoder(data[0][0], data[0][1], data[0][2])
