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
        random collision disadvantage possible.
        => A short code must have a length of 6, alphanumeric and only an underscore as punctuation character
        :return:
        """
        if not url_data["short_code"]:
            alphabet = string.ascii_letters + string.digits + '_'
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
        """
         Shorten a URL, simply shortens a url to a 6 alphanumeric character string
         on an occasion that no short code is given.
         if it already exists or url is empty => an error should be
         triggered.
         ** If short code is longer or shorter than 6 characters but not empty
         a validation check is initiated for an invalid code.
        :param url_data: URL form data a user sends (url and short_code)
        """
        short_code = self.generate_short_code(url_data)
        short_code_key = self.client.key("Urls", short_code)
        entity = datastore.Entity(key=short_code_key)
        exists = self.client.get(key=short_code_key) is not None
        if exists:
            return make_response(jsonify({"error": "Already in use"}), 409)
        elif not (
                url_data["short_code"].__len__() in [6, 0]):
            return make_response(
                jsonify({"error": "The provided URL short code is invalid"}), 412
            )
        elif not url_data["url"]:
            return make_response(jsonify({"error": "URL not found"}), 400)
        else:
            entity.update(
                dict(
                    url=url_data["url"],
                    short_code=short_code,
                    created=datetime.now().isoformat(timespec="minutes"),
                    redirect_count=0,
                )
            )
            self.client.put(entity=entity)
            return make_response(jsonify({"short_code": entity.key.id_or_name}), 200)

    def redirect(self, short_code):
        """
        Redirect to the url and update count and date. Intention is to redirect to a url
        corresponding to the given short code
        => ShortCode *** URL 302 Redirect
        :param short_code: string representing a short code redirect
        """
        code = self.client.get(self.client.key("Urls", short_code))
        code.update({"last_redirect": datetime.now().isoformat(timespec="minutes")})
        code["redirect_count"] += 1
        self.client.put(code)
        if not code:
            return make_response(
                jsonify({"error": "Provided ShortCode not found"}), 404
            )
        response = make_response(redirect(code["url"]), 302)
        response.headers['Location'] = response.location
        return response

    def get_stats(self, short_code):
        """
         Get stats of a URL data object with attributes of when a short code was created,
         how many times its been redirected, and last time it was redirected
         => created, last_redirected, redirect_count + { url and short code }

        :param short_code: A short code to get stats about
        """
        stats = self.client.get(self.client.key("Urls", short_code))
        if not stats:
            return make_response(
                jsonify({"error": "Provided ShortCode not found"}), 404
            )
        return make_response(jsonify(stats), 200)


url_instance = UrlShortener()


def shorten_url():
    """
    Swagger operation id contact to provide functionality
    on Shortening a URL """
    request = connexion.request
    if request.is_json:
        url_data = Url.from_dict(request.get_json())
        return url_instance.shorten(url_data.to_dict())


def redirect_to_url(short_code):
    """
     Swagger operation id to Redirect a short code
     :param short_code: e.g '23dsf_'
     """
    return url_instance.redirect(short_code)


def get_short_code_stats(short_code):
    """
     Redirect stats for a given short code
    :param short_code: e.g '345_er
    """
    return url_instance.get_stats(short_code)
