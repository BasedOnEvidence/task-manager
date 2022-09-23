from django.test import TestCase
from django.urls import reverse

from users.models import User
from labels.models import Label


LABEL_WITHOUT_TASKS_ID = 4


class LabelTests(TestCase):
    fixtures = [
        'users.json', 'statuses.json', 'labels.json', 'tasks.json', 'task_labels_relations.json'
    ]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.label = Label.objects.first()
        self.free_label = Label.objects.get(pk=LABEL_WITHOUT_TASKS_ID)
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
        response = self.client.post(reverse('update_label', kwargs={'pk': self.label.pk}), data={
            'name': 'Test update label'
        })
        self.assertEqual(response.status_code, 302)
        changed_label = Label.objects.get(pk=self.label.pk)
        self.assertEqual(changed_label.name, 'Test update label')

    def test_delete_label(self):
        response = self.client.post(reverse('delete_label', kwargs={'pk': self.free_label.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.free_label.pk)

    def test_delete_label_by_anonymous_user(self):
        self.client.logout()
        response = self.client.post(reverse('delete_label', kwargs={'pk': self.free_label.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        self.assertTrue(Label.objects.filter(pk=self.free_label.pk).exists())

    def test_delete_label_with_tasks(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_label', kwargs={'pk': self.label.pk}))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/labels/')
