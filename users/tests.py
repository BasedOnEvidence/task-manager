from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.test_user = User.objects.first()

    def test_signup_page(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

    def test_create_user(self):
        user_data = {
            'first_name': 'Alex',
            'last_name': 'K',
            'username': 'new_admin',
            'password1': 'Qwerty!@',
            'password2': 'Qwerty!@'
        }
        response = self.client.post(reverse('create_user'), data=user_data)
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username='new_admin')
        self.assertEqual(new_user.first_name, 'Alex')
        self.assertEqual(new_user.last_name, 'K')
        self.assertEqual(new_user.username, 'new_admin')
        bad_user_data = user_data.copy()
        bad_user_data['first_name'] = ''
        bad_user_data['username'] = 'bad_admin'
        response = self.client.post(reverse('create_user'), data=bad_user_data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=bad_user_data.get('username'))
        bad_user_data = user_data.copy()
        bad_user_data['last_name'] = ''
        bad_user_data['username'] = 'bad_admin'
        response = self.client.post(reverse('create_user'), data=bad_user_data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=bad_user_data.get('username'))

    def test_update_user(self):
        self.client.force_login(self.test_user)
        user_data = {
            'first_name': 'New first name',
            'last_name': 'New last name',
            'username': 'new_admin_1',
            'password1': 'Qwerty!@1',
            'password2': 'Qwerty!@1'
        }
        response = self.client.post(
            reverse('update_user', kwargs={'pk': self.test_user.pk}),
            data=user_data
        )
        self.assertEqual(response.status_code, 302)
        changed_user = User.objects.get(pk=1)
        self.assertEqual(changed_user.first_name, 'New first name')
        self.assertEqual(changed_user.last_name, 'New last name')
        self.assertEqual(changed_user.username, 'new_admin_1')
        bad_user_data = user_data.copy()
        bad_user_data['first_name'] = ''
        response = self.client.post(
            reverse('update_user', kwargs={'pk': self.test_user.pk}),
            data=user_data
        )
        self.assertEqual(changed_user.first_name, 'New first name')
        bad_user_data = user_data.copy()
        bad_user_data['last_name'] = ''
        response = self.client.post(
            reverse('update_user', kwargs={'pk': self.test_user.pk}),
            data=user_data
        )
        self.assertEqual(changed_user.last_name, 'New last name')

    def test_delete_user(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse('delete_user', kwargs={'pk': self.test_user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/')
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.test_user.pk)

    def test_delete_user_by_anonymous_user(self):
        response = self.client.post(reverse('delete_user', kwargs={'pk': self.test_user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(User.objects.filter(pk=self.test_user.pk).exists())
