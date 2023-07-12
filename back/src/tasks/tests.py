from base.tests import BaseTestView, RecognizeServersFactory, TasksFactory, UserFactory
from django.test import TestCase
from django.urls import reverse
from tasks.models import PLAY_STATUS_TASK, STOP_STATUS_TASK, StatusTasks


class TasksTest(BaseTestView, TestCase):
    url = reverse('tasks-list')
    fixtures = ['fixtures/task_status.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)

    def test_010_list_tasks(self):
        TasksFactory.create_batch(10)
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

    def test_020_retrieve_task(self):
        task = TasksFactory(model=RecognizeServersFactory.create_batch(10))
        self.client.force_authenticate(self.user)
        response = self.client.get(f'{self.url}{task.id}/')
        self.assertEqual(response.status_code, 200)

    def test_030_update_task(self):
        task = TasksFactory()
        model, model2 = RecognizeServersFactory.create_batch(2)
        data = {
            'alias': '123',
            'model': [model.id, model2.id],
            'period_from': '1992-09-09',
            'period_to': '2023-10-10',
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(f'{self.url}{task.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_040_delete_task(self):
        task = TasksFactory(model=RecognizeServersFactory.create_batch(10))
        self.client.force_authenticate(self.user)
        response = self.client.delete(f'{self.url}{task.id}/')
        self.assertEqual(response.status_code, 204)

    def test_050_play_task(self):
        task = TasksFactory(status=StatusTasks.objects.get(pk=STOP_STATUS_TASK))
        self.client.force_authenticate(self.user)
        response = self.client.post(f'{self.url}{task.id}/play/')
        self.assertEqual(response.status_code, 200)

    def test_050_stop_task(self):
        task = TasksFactory(status=StatusTasks.objects.get(pk=PLAY_STATUS_TASK))
        self.client.force_authenticate(self.user)
        response = self.client.post(f'{self.url}{task.id}/stop/')
        self.assertEqual(response.status_code, 200)
