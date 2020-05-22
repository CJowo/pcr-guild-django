from django.test import TestCase


class GuildTest(TestCase):

    def setUp(self):
        self.client.post('/api/user/register', {'username': 'a12345', 'password': 'password1&*', 'nickname': 'nickname'})
        response = self.client.post('/api/user/login', {'username': 'a12345', 'password': 'password1&*'})
        self.client.cookies = response.cookies

    def test_create(self):
        response = self.client.post('/api/guild/create', {'name': 'aaa'})
        self.assertEqual(response.status_code, 200)
