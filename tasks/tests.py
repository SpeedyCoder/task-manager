from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.models import Task


class ViewsTest(TestCase):
    user_model = get_user_model()

    def setUp(self):
        self.user = self.user_model(username='testuser', email='test@test.com')
        self.user.set_password('qwertyuiop')
        self.user.save()

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

    def test_filter(self):
        self.client.login(username='testuser', password='qwertyuiop')
        Task.objects.create(name='todo', description='', state=Task.STATE.todo)
        Task.objects.create(name='done', description='', state=Task.STATE.done)

        response = self.client.get('/?hide_completed=false', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

        response = self.client.get('/?hide_completed=true', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 1)

    def test_create(self):
        self.client.login(username='testuser', password='qwertyuiop')
        response = self.client.get('/task/', follow=True)
        self.assertEqual(response.status_code, 200)
        form_data = dict(name='Test Name', state=Task.STATE.todo, description='Test Description.')
        response = self.client.post('/task/', data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.filter(**form_data).count(), 1)

    def test_update(self):
        self.client.login(username='testuser', password='qwertyuiop')
        task = Task.objects.create(name='Test Task', description='Test description.', owner=self.user)

        response = self.client.get(f'/task/{task.id}', follow=True)
        self.assertEqual(response.status_code, 200)
        form_data = dict(name='Test Task', state=Task.STATE.in_progress, description='Test')
        response = self.client.post(f'/task/{task.id}', data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        task.refresh_from_db()
        self.assertEqual(task.state, form_data['state'])
        self.assertEqual(task.description, form_data['description'])

    def test_complete(self):
        self.client.login(username='testuser', password='qwertyuiop')
        task = Task.objects.create(name='Test Task', description='Test description.', owner=self.user)

        response = self.client.get(f'/task/{task.id}/complete', follow=True)
        self.assertEqual(response.status_code, 200)

        task.refresh_from_db()
        self.assertEqual(task.state, Task.STATE.done)
        self.assertEqual(task.completed_by, self.user)

    def test_delete(self):
        self.client.login(username='testuser', password='qwertyuiop')
        task_data = dict(name='Test Task', description='Test description.', owner=self.user)
        task = Task.objects.create(**task_data)

        response = self.client.get(f'/task/{task.id}/delete', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Task.objects.filter(**task_data).count(), 0)

    def assert_redirect_to_login(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in str(response.content))

    def test_permissions(self):
        self.client.login(username='testuser', password='qwertyuiop')
        user = self.user_model.objects.create(username='another', email='another@user.com')

        task = Task.objects.create(name='Test Task', description='Test description.', owner=user)

        # User shouldn't be able to edit and delete a task owned by another user,
        # they should be redirected to login page
        response = self.client.get(f'/task/{task.id}', follow=True)
        self.assert_redirect_to_login(response)

        form_data = dict(name='Test Task', description='Test description.', state=Task.STATE.todo)
        response = self.client.post(f'/task/{task.id}', data=form_data, follow=True)
        self.assert_redirect_to_login(response)

        response = self.client.get(f'/task/{task.id}/delete', follow=True)
        self.assert_redirect_to_login(response)

        # They should be able to mark it as completed
        response = self.client.get(f'/task/{task.id}/complete', follow=True)

        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.state, Task.STATE.done)
        self.assertEqual(task.completed_by, self.user)
