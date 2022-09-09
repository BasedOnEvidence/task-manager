from django.test import TestCase, modify_settings
from django.urls import reverse

from users.models import User


@modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.test_user = User.objects.get(pk=1)

    def test_signup_page(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

    def test_create_user(self):
        response = self.client.post(reverse('create_user'), data={
            'first_name': 'Alex',
            'last_name': 'K',
            'username': 'new_admin',
            'password1': 'Qwerty!@',
            'password2': 'Qwerty!@'
        })
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='new_admin')
        self.assertEqual(new_user.first_name, 'Alex')
        self.assertEqual(new_user.last_name, 'K')
        self.assertEqual(new_user.username, 'new_admin')

    def test_update_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('update_user', kwargs={'pk': self.test_user.pk}), data={
            'first_name': 'New first name',
            'last_name': 'New last name',
            'username': 'new_admin_1',
            'password1': 'Qwerty!@1',
            'password2': 'Qwerty!@1'
        })
        self.assertEqual(response.status_code, 302)
        changed_user = User.objects.get(pk=1)
        self.assertEqual(changed_user.first_name, 'New first name')
        self.assertEqual(changed_user.last_name, 'New last name')
        self.assertEqual(changed_user.username, 'new_admin_1')

    def test_delete_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('delete_user', kwargs={'pk': self.test_user.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.test_user.pk)
