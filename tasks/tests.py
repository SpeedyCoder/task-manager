from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.models import Task


class ViewsTest(TestCase):
    user_model = get_user_model()

    def setUp(self):
        user = self.user_model(username='testuser', email='test@test.com')
        user.set_password('qwertyuiop')
        user.save()

    def test_login(self):
        response = self.client.get('/login/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_auth(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.url)

    def test_list(self):
        self.client.login(username='testuser', password='qwertyuiop')
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        self.client.login(username='testuser', password='qwertyuiop')
        response = self.client.get('/task/', follow=True)
        self.assertEqual(response.status_code, 200)
        form_data = dict(name='Test Name', state=Task.STATE.todo, description='Test Description.')
        response = self.client.post('/task/', data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(**form_data).count(), 1)
