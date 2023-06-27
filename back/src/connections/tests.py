from base.tests import BaseTestView, ConnectionsFactory, UserFactory
from connections.models import Connections
from django.test import TestCase
from rest_framework.reverse import reverse


class ConnectionsViewTest(BaseTestView, TestCase):
    url = reverse('connections-list')
    fixtures = ['fixtures/connect_status.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def test_010_get_list_connections(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_020_create_connections(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 201)

    def test_030_partial_update(self):
        self.client.force_authenticate(self.user)
        data = {
            'alias': '123',
            'db_status': 1,
        }
        connection: Connections = ConnectionsFactory()
        response = self.client.put(f'{self.url}{connection.id}/', data)
        connection = Connections.objects.get(pk=connection.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(connection.alias, '123')

    def test_040_delete_connection(self):
        self.client.force_authenticate(self.user)
        connection: Connections = ConnectionsFactory()
        response = self.client.delete(f'{self.url}{connection.id}/')
        self.assertEqual(response.status_code, 204)

    def test_050_check_connections(self):
        self.client.force_authenticate(self.user)
        connection: Connections = ConnectionsFactory()
        response = self.client.get(f'{self.url}{connection.id}/refresh/')
        self.assertEqual(response.status_code, 200)
