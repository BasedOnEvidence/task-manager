from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import User
from tasks.models import Task
from labels.models import Label


PERFORMER_USER_ID = 2
ADDITIONAL_LABEL_ID = 2
NEW_LABEL_ID = 3
ADDITIONAL_STATUS_ID = 2


class TaskTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self) -> None:
        self.author = User.objects.first()
        self.perfomer = User.objects.get(pk=PERFORMER_USER_ID)
        self.status = Status.objects.first()
        self.new_stats = Status.objects.get(pk=ADDITIONAL_STATUS_ID)
        self.task = Task.objects.first()
        self.label = Label.objects.first()
        self.additional_label = Label.objects.get(pk=ADDITIONAL_LABEL_ID)
        self.new_label = Label.objects.get(pk=NEW_LABEL_ID)
        self.client.force_login(self.author)

    def test_list_tasks(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/list.html')

    def test_view_task(self):
        response = self.client.get(reverse('view_task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/view.html')

    def test_create_task(self):
        response = self.client.post(reverse('create_task'), data={
            'name': 'Test task',
            'description': 'Text example',
            'author': self.author.pk,
            'executor': self.perfomer.pk,
            'status': self.status.pk,
            'labels': [self.label.pk, self.additional_label.pk]
        })
        self.assertEqual(response.status_code, 302)
        new_task = Task.objects.get(name='Test task')
        self.assertEqual(new_task.name, 'Test task')
        self.assertEqual(new_task.description, 'Text example')
        self.assertEqual(new_task.author.pk, self.author.pk)
        self.assertEqual(new_task.executor.pk, self.perfomer.pk)
        self.assertEqual(new_task.status.pk, self.status.pk)
        self.assertEqual(new_task.labels.all()[0].pk, self.label.pk)
        self.assertEqual(new_task.labels.all()[1].pk, self.additional_label.pk)

    def test_update_task(self):
        response = self.client.post(reverse('update_task', kwargs={'pk': self.task.pk}), data={
            'name': 'Test update task',
            'description': 'Text update description',
            'executor': self.author.pk,
            'status': self.new_stats.pk,
            'labels': [self.label.pk, self.new_label.pk]
        })
        self.assertEqual(response.status_code, 302)
        changed_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(changed_task.name, 'Test update task')
        self.assertEqual(changed_task.description, 'Text update description')
        self.assertEqual(changed_task.author.pk, self.author.pk)
        self.assertEqual(changed_task.executor.pk, self.author.pk)
        self.assertEqual(changed_task.status.pk, self.new_stats.pk)
        self.assertEqual(changed_task.labels.all()[0].pk, self.label.pk)
        self.assertEqual(changed_task.labels.all()[1].pk, self.new_label.pk)

    def test_delete_task(self):
        response = self.client.post(reverse('delete_task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)

    def test_delete_task_by_non_author(self):
        self.client.force_login(self.perfomer)
        response = self.client.post(reverse('delete_task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_by_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('delete_task', kwargs={'pk': self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
