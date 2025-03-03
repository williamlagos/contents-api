from django.test import Client, TestCase


class ContentTestCase(TestCase):
    """Test case for the content views."""

    def setUp(self):
        self.client = Client()

    def test_read_main(self):
        """Test the root view."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"health": "OK"})
