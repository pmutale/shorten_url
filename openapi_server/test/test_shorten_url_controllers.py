import json

from openapi_server.test import BaseTestCase

URL = 'https://www.google.com'
SHORT_CODE = 'gooL1_'

class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_shorten_url(self):
        """Test case for shortening a url"""
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'url': URL,
            'short_code': SHORT_CODE
        }
        response = self.client.open(
            '/urls/shorten',
            method='POST',
            headers=headers,
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_redirect(self):
        url = 'https://www.google.com'
        short_code = SHORT_CODE
        response = self.client.get(f'/urls/{short_code}')
        self.assertEqual(response.status_code, 302, 'URLS matching redirect successful')

    def test_url_data(self):
        short_code = SHORT_CODE
        response = self.client.open(f'/urls/{short_code}/stats')
        self.assert200(response)
