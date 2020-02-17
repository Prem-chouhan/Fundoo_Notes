import argparse
import json
import jwt
import cgi
import os

from models import dbmanipulate
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.userservice import user
from view.noteservices import Notes
from view.response import Response
from auth.login_required import is_authenticated, response
from config.redis_connection import RedisService

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()

    def _html(self, message=None):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()

        if self.path == '/register':
            with open('templates/register.html', 'r') as f:
                html_string_register = f.read()
                self.wfile.write(self._html(html_string_register))

        elif self.path == '/login':
            with open('templates/login.html', 'r') as f:
                html_string_login = f.read()
                self.wfile.write(self._html(html_string_login))

        elif self.path == '/forgot':
            with open('templates/forgot.html', 'r') as f:
                html_string_login = f.read()
                self.wfile.write(self._html(html_string_login))

        elif '/reset' in self.path:
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            token = query_components["token"][0]
            with open('templates/reset.html', 'r') as f:
                html_string_register = f.read()
                output = html_string_register.format(result=token)
                self.wfile.write(self._html(output))

        elif self.path == '/listing':
            obj = user
            catch, respon, res = obj.listing_notes(self)
            response_data = {'success': True, "data": [],
                             "message": "This is listing Of is_pinned{}{}{}".format(catch, respon, res)}
            Response(self).jsonResponse(status=404, data=response_data)

        else:
            # response_data = {'success': False, "data": [], "message": "URL Invalid"}
            # Response(self).jsonResponse(status=404, data=response_data)
            with open('templates/error.html', 'r') as f:
                html_string_register = f.read()
                # self.wfile.write(self._html(html_string_register))

    @is_authenticated
    def do_POST(self):
        obj = user
        obj_note = Notes

        if self.path == '/register':
            response_data = obj.register_user(self)
            Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/login':
            response_data = obj.login_user(self)
            Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/forgot':
            response_data = obj.forgot_password(self)
            Response(self).jsonResponse(status=404, data=response_data)

        elif '/reset' in self.path:
            obj.update_confirmation(self, self.path)
            try:
                from urllib.parse import urlparse, parse_qs
                query_components = parse_qs(urlparse(self.path).query)
                token = query_components["token"][0]
                token = jwt.decode(token, "secret", algorithms='HS256')
                key = token["email_id"]
                obj = user
                response_data = obj.update_confirmation(self, key)
                Response(self).jsonResponse(status=404, data=response_data)

            except json.decoder.JSONDecodeError:
                response_data = {'success': False, "data": [], "message": "Json decode Error raised"}
                Response(self).jsonResponse(status=404, data=response_data)

            except jwt.exceptions.DecodeError:
                response_data = {'success': False, "data": [], "message": "JWT decode error raised"}
                Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/api/note/insert':
            response_data = obj_note.insert_notes(self)
            Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/api/profile':
            response_data = obj.updateProfile(self)
            Response(self).jsonResponse(status=404, data=response_data)

        else:
            response_data = {'success': False, "data": [], "message": "URL Invalid"}
            Response(self).jsonResponse(status=404, data=response_data)

    @is_authenticated
    def do_PUT(self):
        if self.path == '/api/note/update':
            obj = Notes
            response_data = obj.update_notes(self)
            Response(self).jsonResponse(status=404, data=response_data)

    @is_authenticated
    def do_DELETE(self):
        if self.path == '/api/note/delete':
            obj = Notes
            response_data = obj.delete_notes(self)
            Response(self).jsonResponse(status=404, data=response_data)
