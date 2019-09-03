import secrets
import string
from datetime import datetime

import connexion
from flask import make_response, jsonify, redirect

from google.cloud import datastore

from openapi_server.models.url import Url


class UrlShortener:
    """ A URL shortener class instance """

    def __init__(self):
        self.client = datastore.Client()

    @staticmethod
    def generate_short_code(url_data):
        """
        A short code that will be assigned to a URL. This has a minimal
        random collision disadvantage possible
        :return:
        """
        if not url_data["short_code"]:
            alphabet = string.ascii_letters + string.digits + string.punctuation
            while True:
                random_id = "".join(secrets.choice(alphabet) for i in range(6))
                if (
                    any(c.islower() for c in random_id)
                    and any(c.isupper() for c in random_id)
                    and sum(c.isdigit() for c in random_id) >= 3
                ):
                    break
            return random_id
        else:
            return url_data["short_code"]

    def shorten(self, url_data):
        """Shorten a URL """
        short_code = self.generate_short_code(url_data)
        short_code_key = self.client.key("Urls", short_code)
        entity = datastore.Entity(key=short_code_key)
        exists = self.client.get(key=short_code_key) is not None
        if exists:
            return make_response(jsonify({"info": "Already in use"}), 409)
        elif not (url_data["short_code"].__len__() > 6 or (url_data["short_code"].__len__() == 0)):
            return make_response(
                jsonify({"info": "The provided URL short code is invalid"}), 412
            )
        elif not url_data["url"]:
            return make_response(jsonify({"error": "URL not found"}), 400)
        else:
            entity.update(
                dict(
                    url=url_data["url"],
                    short_code=short_code,
                    created=datetime.now(),
                    redirect_count=0,
                )
            )
            self.client.put(entity=entity)
            return make_response(jsonify({"short_code": entity.key.id_or_name}), 200)

    def redirect(self, short_code):
        """
        Redirect the url and update count and date
        :param short_code: string representing a short code redirect
        """
        code = self.client.get(self.client.key("Urls", short_code))
        code.update({"last_redirect": datetime.now()})
        code["redirect_count"] += 1
        self.client.put(code)
        if not code:
            return make_response(
                jsonify({"error": "Provided ShortCode not found"}), 404
            )
        return make_response(redirect(code["url"]), 302)

    def get_stats(self, short_code):
        """ Get stats of a URL"""
        stats = self.client.get(self.client.key("Urls", short_code))
        if not stats:
            return make_response(
                jsonify({"error": "Provided ShortCode not found"}), 404
            )
        return make_response(jsonify(stats), 200)


url_instance = UrlShortener()


def shorten_url():
    """ Shorten a URL """
    request = connexion.request
    if request.is_json:
        url_data = Url.from_dict(request.get_json())
        return url_instance.shorten(url_data.to_dict())


def redirect_to_url(short_code):
    """ Redirect controller """
    return url_instance.redirect(short_code)


def get_short_code_stats(short_code):
    """ Redirect stats for a given short code """
    return url_instance.get_stats(short_code)
