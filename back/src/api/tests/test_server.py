from rest_framework.test import APITestCase

from api.transcribation_server import TranscriptionServer


class ServerTest(APITestCase):

    def test_010_connect_to_server(self):
        context = {
            'ip': '172.17.0.1',
            'port': '5432',
            'db_login': 'admin',
            'db_password': '000092',
            'db_name': 'test_sprut',
            'db_system': {
                'name': 'Postgres'
            },
            'alias': '123',
        }
        status, response = TranscriptionServer().check_connection(context)
        self.assertTrue(status)
