from django.test import TestCase, modify_settings
from django.urls import reverse

from statuses.models import Status
from users.models import User


@modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class UserTests(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_status'), data={
            'name': 'test',
        })
        self.assertEqual(response.status_code, 302)
        new_status = Status.objects.get(name='test')
        self.assertEqual(new_status.name, 'test')

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('update_status', kwargs={'pk': self.status.pk}), data={
            'name': 'new_name',
        })
        self.assertEqual(response.status_code, 302)
        changed_status = Status.objects.get(pk=self.status.pk)
        self.assertEqual(changed_status.name, 'new_name')

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_status', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status.pk)
