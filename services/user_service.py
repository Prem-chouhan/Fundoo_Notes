

class UserLogic:

    def register_logic(self, data, id, present):
        response_data = {'success': True, "data": [], "message": ""}
        if not present:
            response_data.update(
                {"message": "Email Format is Invalid please Re-enter Email", "success": False})
            return response_data
        else:
            if id is None:
                email = data['email']
                password = data['password']
                object.insert_user(email, password)
                response_data.update({"success": True, "data": [], "message": "Registration Done Successfully"})
                return response_data
            else:
                response_data.update({"message": "Email Already Exists", "success": False})
                return response_data

    def login_logic(self):
        pass