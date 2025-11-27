from django.test import TestCase

class CoreIndexTest(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello from Django skeleton')
