import jwt
from view.response import Response
from models.dbmanipulate import model
from config.redis_connection import RedisService

def response(success=False, message='something went wrong', data=[]):
    response = {'success': success,
                "message": message,
                "data": data, }

    return response



def is_authenticated(method):
    def authenticate_user(self):
        """
        this function is used to decode and check whether the user is authorized user or not
        :param catch:
        True:return:
        """

        try:
            print(self.path, type(self.path))
            if self.path in ['/api/note/insert', '/api/note/delete', '/api/note/update']:
                token = self.headers['token']
                payload = jwt.decode(token, "secret", algorithms='HS256')
                id= payload['id']
                redis_obj = RedisService()
                token = redis_obj.get(id)
                if token is None:
                    raise ValueError("You Need To Login First")
                return method(self)
            else:
                return method(self)


        except jwt.ExpiredSignatureError:
            # return 'Signature expired. Please log in again.'
            # response['message']="Signature expired. Please log in again."
            res = response(message="Signature expired. Please log in again.")
            Response(self).jsonResponse(status=404, data=res)

        except jwt.DecodeError:
            # return "Wrong Token"

            res = response(message="DecodeError")

            Response(self).jsonResponse(status=404, data=res)

        except jwt.InvalidTokenError:
            # return 'Invalid token. Please log in again.'
            res = response(message="InvalidTokenError")

            Response(self).jsonResponse(status=404, data=res)

    return authenticate_user
