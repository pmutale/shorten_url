# coding: utf-8

from __future__ import absolute_import

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Url(Model):
    """
        Model to transpire URL data
    """

    def __init__(self, url=None, short_code=None):
        """
        URL

        :param url: The url string
        :type url: str
        :param short_code: A shortened URL code
        :type short_code: str
        """
        self.openapi_types = {
            'url': str,
            'short_code': str,
        }

        self.attribute_map = {
            'url': 'url',
            'short_code': 'short_code',
        }

        self._url = url
        self._short_code = short_code

    @classmethod
    def from_dict(cls, dikt) -> 'Url':
        """Returns the dict as a model
        :param dikt: A dict.
        :type: dict
        :return:  A serialized url
        :rtype: Url
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self):
        """Property the url string
        :return: The URL text
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url string
        :param url: A url string
        :rtype url: str
        """
        if url is None:
            raise ValueError('URL value must not be empty')

        self._url = url

    @property
    def short_code(self):
        """Gets the short code string"""
        return self._short_code

    @short_code.setter
    def short_code(self, short_code):
        """Sets the short code string"""
        self._short_code = short_code
