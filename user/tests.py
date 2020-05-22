from django.test import TestCase

from .models import User


class UserTest(TestCase):

    def test_register(self):
        response = self.client.post('/api/user/register', {'username': 'a12345', 'password': 'password1&*', 'nickname': 'nickname'})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        User.objects.create(**{'username': 'a12345', 'password': 'password1&*', 'nickname': 'nickname'}).set_password('password1&*')
        response = self.client.post('/api/user/login', {'username': 'a12345', 'password': 'password1&*'})
        self.assertEqual(response.status_code, 200)

    def test_refresh_token(self):
        User.objects.create(**{'username': 'a12345', 'password': 'password1&*', 'nickname': 'nickname'}).set_password('password1&*')
        response = self.client.post('/api/user/login', {'username': 'a12345', 'password': 'password1&*'})
        self.client.cookies = response.cookies
        response = self.client.get('/api/user/refresh_token')
        self.assertEqual(response.status_code, 200)
    
    def test_edit(self):
        User.objects.create(**{'username': 'a12345', 'password': 'password1&*', 'nickname': 'nickname'}).set_password('password1&*')
        response = self.client.post('/api/user/login', {'username': 'a12345', 'password': 'password1&*'})
        self.client.cookies = response.cookies
        response = self.client.post('/api/user/edit', {'nickname': 'new_nickname'})
        user = User.objects.get(username='a12345')
        self.assertEqual(user.nickname, 'new_nickname')