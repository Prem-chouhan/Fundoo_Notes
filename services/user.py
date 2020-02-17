from datetime import datetime, timedelta
from auth.login_required import response
import jwt
from config.redis_connection import RedisService
from vendor.smtp import smtp
from models.dbmanipulate import model

# 120 mins
JWT_EXP_DELTA_SECONDS = 72000

object = model()


class Users:

    def register(self, data, id, present):
        response_data = {'success': True, "data": [], "message": ""}

        if not present:
            response_data.update(
                {"message": "Email Format is Invalid please Re-enter Email", "success": False})
            return response_data
        else:
            if id is None:
                # email = data['email']
                # password = data['password']
                # table_name = 'user'
                object.insert(data, table_name='user')
                response_data.update({"success": True, "data": [], "message": "Registration Done Successfully"})
                return response_data
            else:
                response_data.update({"message": "Email Already Exists", "success": False})
                return response_data

    def login(self, id):
        if id:
            payload = {
                'id': id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            encoded_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
            # print(encoded_token)
            redis_obj = RedisService()
            # print(id[0])
            redis_obj.set(id[0], encoded_token)
            response_data = response(success=True, message="Login Successfully", data=[{
                "token": encoded_token
            }])

        return response_data

    def forgot(self, schema, host, data, present):
        response_data = {'success': True, "data": [], "message": ""}
        if not present:
            response_data.update({"success": False, "message": "Wrong Credentials"})
            return response_data
        else:
            encoded = jwt.encode({"email_id": data}, 'secret', algorithm='HS256').decode("utf-8")
            message = f"{schema}://{host}/reset/?token={encoded}"
            obj = smtp()
            obj.SmtpConnect(data, message)
            response_data.update({"success": True, "message": "Successfully sent mail"})
        return response_data

    def reset(self, data, key):
        object.update_password(data, key)
        response_data = {'success': False, "data": [], "message": "Password Updated Successfully"}
        return response_data

    def profile(self, profile_data):
        from models.dbmanipulate import model
        obj = model()
        obj.update_profile(profile_data)
        print(profile_data)

