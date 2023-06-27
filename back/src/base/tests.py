import factory
from connections.models import Connections, ConnectionsStatus, DatabaseSystems
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework.test import APIClient
from tasks.models import RecognizeServers, StatusTasks, Tasks, TaskType

faker = Faker(['ru_Ru'])


class BaseTestView:
    url: str

    def setUp(self) -> None:
        self.client = APIClient()


class DatabaseSystemFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseSystems
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'system %d' % n)


class DatabaseStatusFactory(DjangoModelFactory):
    class Meta:
        model = ConnectionsStatus
        django_get_or_create = ('status_name',)

    status_name = factory.Sequence(lambda n: 'status %d' % n)


class ConnectionsFactory(DjangoModelFactory):
    class Meta:
        model = Connections
        django_get_or_create = ('alias',)

    alias = factory.Sequence(lambda n: 'test alias %d' % n)
    db_system = factory.SubFactory(DatabaseSystemFactory)
    db_status = factory.SubFactory(DatabaseStatusFactory)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = faker.word()
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)


class StatusTaskFactory(DjangoModelFactory):
    class Meta:
        model = StatusTasks
        django_get_or_create = ('status',)

    status = factory.Sequence(lambda n: 'status %d' % n)


class TaskTypeFactory(DjangoModelFactory):
    class Meta:
        model = TaskType

    name = factory.Sequence(lambda n: 'name %d' % n)


class RecognizeServersFactory(DjangoModelFactory):
    class Meta:
        model = RecognizeServers

    name = faker.word()
    short_name = faker.bothify('######')
    ip = faker.ipv4()
    port = faker.numerify('#####')


class TasksFactory(DjangoModelFactory):
    class Meta:
        model = Tasks
        django_get_or_create = ('alias',)

    alias = factory.Sequence(lambda n: 'test alias %d' % n)
    db = factory.SubFactory(ConnectionsFactory)
    task_type = factory.SubFactory(TaskTypeFactory)

    @factory.post_generation
    def model(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for model in extracted:
                self.model.add(model)
