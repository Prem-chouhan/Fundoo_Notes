import os, \
    sys, \
    jwt, \
    cgi, \
    smtplib, \
    base64

from config.redis_connection import RedisService
from view.response import Response
from models.dbmanipulate import model
from auth.login_required import response
from vendor.smtp import smtp
from services.user import Users
from view.utils import Utility
from services.notes import Note

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 100000000

obj_model = model()
obj_user = Users()
my_val = Utility()
obj_note = Note()


class user:

    def register_user(self):
        """
        Here Registration of the user is done and it will check if the customers email is existing in database or not if present response is sent
        and if not present registration is done
        no return type:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        form_keys = list(form.keys())
        if len(form_keys) < 2:
            response_data.update({'success': False, "data": [], "message": " some values are missing"})
            return response_data
        data = {}
        data['email'] = form['email'].value
        data['password'] = form['password'].value
        email = data['email']
        id = obj_model.read_email(email)
        present = my_val.email_validate(email)
        catch_response = obj_user.register(data, id, present)
        return catch_response

    def login_user(self):
        """
        Here User can login and if The username already exists then it will give response or else
        it will give response of Login done successfully
        no return :return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        form_keys = list(form.keys())
        if 'email' and 'password' in form_keys:
            data = {}
            data['email'] = form['email'].value
            data['password'] = form['password'].value
            email = data['email']
            print(email)
            id = obj_model.read_email(email=email)
            response_data = obj_user.login(id)
            return response_data
        else:
            Response(self).jsonResponse(status=400, data=response(message="credentials are missing"))

    def forgot_password(self):
        """
        Here if User Forgot Password so can change password and here If want to reset he have to give email and then
        link will be sent to email and with that link the password will be reset
        no return :return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        data = {}
        data['email'] = form['email'].value
        data = data['email']
        schema = self.protocol_version.split('/')[0]
        host = self.headers['host']
        present = obj_model.read_email(data)
        response = obj_user.forgot(schema, host, data, present)
        return response

    def update_confirmation(self, key):
        """
        here password will be updated and response will be show password updated
        Successfully
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['password'] = form['password'].value
        response_data = obj_user.reset(data, key)
        return response_data



    # def update_notes(self):
    #     """
    #     Here record is Updated in table and response is shown
    #     no return:return:
    #     """
    #     form = cgi.FieldStorage(
    #         fp=self.rfile,
    #         headers=self.headers,
    #         environ={'REQUEST_METHOD': 'POST',
    #                  'CONTENT_TYPE': self.headers['Content-Type'],
    #                  })
    #     data = {}
    #     data['id'] = form['id'].value
    #     data['tittle'] = form['tittle'].value
    #     response_data = obj_note.update_note(data)
    #     return response_data

    def delete_notes(self):
        """
        Here record is Deleted in table and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['id'] = form['id'].value
        response_data = obj_note.delete_note(data)
        return response_data

    def read_note(self):
        """
        Here record is Read in table and response is shown
        no return:return:
        """
        object = model()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tablename'] = form['tablename'].value
        object.query_read(data)
        response_data = {'success': True, "data": [], "message": "Read Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def create_note(self):
        """
         Here  creation of  table is done and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': "POST",
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tablename'] = form['tablename'].value
        obj_model.query_create(data)
        response_data = {'success': True, "data": [], "message": "created table Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def updateProfile(self):
        token = self.headers['token']
        payload = jwt.decode(token, "secret", algorithms='HS256')
        id = payload['id']
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                  'CONTENT_TYPE': self.headers[
                                                                                      'Content-Type'], })

            filename = form['upfile'].filename
            data = form['upfile'].file.read()
            open("./media/%s" % filename, "wb").write(data)
            profile_data = {
                'profile_path': f'./media/{filename}',
                'id': id
            }
            flag = my_val.validate_file_extension(profile_data)
            check = my_val.validate_file_size(profile_data)
            if flag and check:
                obj_user.profile(profile_data)
                response_data = {'success': True, "data": [], "message": "Profile Updated Successfully"}
                return response_data
            else:
                response_data = {'success': True, "data": [], "message": "Unsupported file extension"}
                return response_data

    def listing_notes(self):
        reaminders = obj_model.remainders()
        archive = obj_model.archives()
        trash = obj_model.trashed()
        return reaminders, archive, trash

    # def authenticate_user(self, catch):
    #     """
    #     this function is used to decode and check whether the user is authorized user or not
    #     :param catch:
    #     True:return:
    #     """
    #     try:
    #         jwt_decode = jwt.decode(catch, "secret", algorithms='HS256')
    #         data = jwt_decode['username']
    #         obj = DbManaged()
    #         flag = obj.read_email(data)
    #         return flag
    #     except jwt.ExpiredSignatureError:
    #         # return 'Signature expired. Please log in again.'
    #         response_data = {'success': False, "data": [], "message": "Signature expired. Please log in again."}
    #         Response(self).jsonResponse(status=404, data=response_data)
    #
    #     except jwt.DecodeError:
    #         # return "Wrong Token"
    #         response_data = {'success': False, "data": [], "message": "Wrong Token"}
    #         Response(self).jsonResponse(status=404, data=response_data)
    #
    #     except jwt.InvalidTokenError:
    #         # return 'Invalid token. Please log in again.'
    #         response_data = {'success': False, "data": [], "message": "Invalid token. Please log in again."}
    #         Response(self).jsonResponse(status=404, data=response_data)