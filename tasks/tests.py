from django.test import TestCase
from django.contrib.auth import get_user_model


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

    def test_home(self):
        self.client.login(username='testuser', password='qwertyuiop')
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
