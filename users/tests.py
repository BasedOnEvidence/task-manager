from django.test import TestCase, modify_settings
from django.urls import reverse
from django.contrib.auth import get_user_model


@modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.test_user = get_user_model().objects.get(pk=1)
        self.first_name = 'Alex'
        self.last_name = 'K'
        self.username = 'new_admin'
        self.password = 'Qwerty!@'
        self.new_password = 'Qwerty$#'
        self.new_user_name = 'old_admin'

    def test_signup_page(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

    def test_create_user(self):
        response = self.client.post(reverse('create_user'), data={
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 4)

    def test_update_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('update_user', kwargs={'pk': self.test_user.pk}), data={
            'first_name': self.test_user.first_name,
            'last_name': self.test_user.last_name,
            'username': self.new_user_name,
            'password1': self.new_password,
            'password2': self.new_password
        })
        self.assertEqual(response.status_code, 302)
        changed_user = get_user_model().objects.get(pk=self.test_user.pk)
        self.assertEqual(changed_user.username, self.new_user_name)

    def test_delete_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('delete_user', kwargs={'pk': self.test_user.pk}))
        self.assertEqual(response.status_code, 302)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)
