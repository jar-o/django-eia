from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client

setup_test_environment()
client = Client()

class BasicTests(TestCase):

    def test_statuscodes(self):
        self.assertEqual(client.get('/').status_code, 200)
        self.assertEqual(client.get('/api').status_code, 301)
        self.assertEqual(client.get('/api/annual').status_code, 200)

    def test_contenttype(self):
        self.assertEqual(client.get('/')['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(client.get('/api')['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(client.get('/api/annual')['Content-Type'], 'application/json')
