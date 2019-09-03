import json

from openapi_server.test import BaseTestCase

URL = "https://www.google.com"
SHORT_CODE = "gooL1_"


class CustomAssertMethods(BaseTestCase):
    def assert409(self, response, message):
        """ Already in use"""
        self.assertStatus(response, 409, message)

    def assert412(self, response, message):
        """ Invalid short code"""
        self.assertStatus(response, 412, message)


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_shorten_url(self):
        """Test case for shortening a url"""
        headers = {"Content-Type": "application/json"}
        data = {"url": URL, "short_code": SHORT_CODE}
        response = self.client.open(
            "/urls/shorten",
            method="POST",
            headers=headers,
            data=json.dumps(data),
            content_type="application/json",
        )
        if response.status_code == 409:
            CustomAssertMethods().assert409(
                response=response,
                message=f'Response body is: {response.data.decode("utf-8")}',
            )
        elif response.status_code == 400:
            self.assert400(
                response, f'Response body is : {response.data.decode("utf-8")}'
            )
        elif response.status_code == 412:
            CustomAssertMethods().assert412(
                response, f'Response body is : {response.data.decode("utf-8")}'
            )
        elif response.status_code == 200:
            self.assert200(
                response, f'Response body is : {response.data.decode("utf-8")}'
            )

    def test_redirect(self):
        url = "https://www.google.com"
        short_code = SHORT_CODE
        response = self.client.get(f"/urls/{short_code}")
        self.assert_redirects(response, url)

    def test_url_data(self):
        short_code = SHORT_CODE
        response = self.client.open(f"/urls/{short_code}/stats")
        self.assert200(response)
