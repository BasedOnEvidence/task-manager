from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from users.models import User


class UserTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)
        self.status_name = 'test'
        self.new_status_name = 'new_name'

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_status'), data={
            'name': self.status_name,
        })
        self.assertEqual(response.status_code, 302)
        statuses = Status.objects.all()
        self.assertEqual(statuses.count(), 5)

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('update_status', kwargs={'pk': self.status.pk}), data={
            'name': self.new_status_name,
        })
        self.assertEqual(response.status_code, 302)
        changed_status = Status.objects.get(pk=self.status.pk)
        self.assertEqual(changed_status.name, self.new_status_name)

    def test_delete_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_status', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        statuses = Status.objects.all()
        self.assertEqual(statuses.count(), 3)
