from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import User


class UserTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_list_statuses(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/list.html')

    def test_create_status(self):
        response = self.client.post(reverse('create_status'), data={
            'name': 'test',
        })
        self.assertEqual(response.status_code, 302)
        new_status = Status.objects.get(name='test')
        self.assertEqual(new_status.name, 'test')

    def test_update_status(self):
        response = self.client.post(reverse('update_status', kwargs={'pk': self.status.pk}), data={
            'name': 'new_name',
        })
        self.assertEqual(response.status_code, 302)
        changed_status = Status.objects.get(pk=self.status.pk)
        self.assertEqual(changed_status.name, 'new_name')

    def test_delete_status(self):
        response = self.client.post(reverse('delete_status', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status.pk)

    def test_delete_status_by_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('delete_status', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

    def test_delete_status_with_tasks(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_status', kwargs={'pk': 2}))
        self.assertTrue(Status.objects.filter(pk=2).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/statuses/')
