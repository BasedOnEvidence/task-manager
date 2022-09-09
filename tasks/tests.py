from django.test import TestCase, modify_settings
from django.urls import reverse

from statuses.models import Status
from users.models import User
from tasks.models import Task
from labels.models import Label


@modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class TaskTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

    def test_create_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_task'), data={
            'name': 'Test task',
            'description': 'Text example',
            'author': 1,
            'executor': 2,
            'status': 1,
            'labels': [1, 2]
        })
        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(name='Test task')
        self.assertEqual(new_task.name, 'Test task')
        self.assertEqual(new_task.description, 'Text example')
        self.assertEqual(new_task.author.pk, 1)
        self.assertEqual(new_task.executor.pk, 2)
        self.assertEqual(new_task.status.pk, 1)
        self.assertEqual(new_task.labels.all()[0].pk, 1)
        self.assertEqual(new_task.labels.all()[1].pk, 2)

    def test_update_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('update_task', kwargs={'pk': 1}), data={
            'name': 'Test update task',
            'description': 'Text update description',
            'executor': 3,
            'status': 2,
            'labels': [2, 3]
        })
        self.assertEqual(response.status_code, 302)
        changed_task = Task.objects.get(pk=1)
        self.assertEqual(changed_task.name, 'Test update task')
        self.assertEqual(changed_task.description, 'Text update description')
        self.assertEqual(changed_task.author.pk, 1)
        self.assertEqual(changed_task.executor.pk, 3)
        self.assertEqual(changed_task.status.pk, 2)
        self.assertEqual(changed_task.labels.all()[0].pk, 2)
        self.assertEqual(changed_task.labels.all()[1].pk, 3)

    def test_delete_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=1)
