from models.dbmanipulate import model

object = model()


class Note:
    def insert_note(self, data):
        object.insert(data, table_name)
        response_data = {'success': True, "data": [], "message": "Inserted Successfully"}
        return response_data

    def update_note(self, data):
        object.update(data)
        response_data = {'success': True, "data": [], "message": "Updated Successfully"}
        return response_data

    def delete_note(self, data):
        object.delete(data)
        response_data = {'success': True, "data": [], "message": "Deleted Successfully"}
        return response_data
