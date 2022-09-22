from django.test import TestCase, modify_settings
from django.urls import reverse

from users.models import User
from labels.models import Label


@modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})
class LabelTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json', 'task_labels_relations.json']

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_list_labels(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/list.html')

    def test_create_label(self):
        response = self.client.post(reverse('create_label'), data={
            'name': 'Test label',
        })
        self.assertEqual(response.status_code, 302)
        new_label = Label.objects.get(name='Test label')
        self.assertEqual(new_label.name, 'Test label')

    def test_update_label(self):
        response = self.client.post(reverse('update_label', kwargs={'pk': 1}), data={
            'name': 'Test update label'
        })
        self.assertEqual(response.status_code, 302)
        changed_task = Label.objects.get(pk=1)
        self.assertEqual(changed_task.name, 'Test update label')

    def test_delete_label(self):
        response = self.client.post(reverse('delete_label', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=4)

    def test_delete_label_by_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('delete_label', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(Label.objects.filter(pk=4).exists())

    def test_delete_label_with_tasks(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_label', kwargs={'pk': 2}))
        self.assertTrue(Label.objects.filter(pk=2).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/labels/')
