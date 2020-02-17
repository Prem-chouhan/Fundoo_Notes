from services.notes import Note
import jwt
import cgi
obj_note = Note()


class Notes:
    def insert_notes(self):
        """
        Here record is inserted in table and response is shown
        :return:response_data
        """
        token = self.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = payload['id']
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tittle'] = form['tittle'].value
        data['description'] = form['description'].value
        data['color'] = form['color'].value
        data['is_pinned'] = form['is_pinned'].value
        data['is_archived'] = form['is_archived'].value
        data['is_trashed'] = form['is_trashed'].value
        data['user_id'] = id
        response_data = obj_note.insert_note(data)
        return response_data

    def update_notes(self):
        """
        Here record is Updated in table and response is shown
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
        data['tittle'] = form['tittle'].value
        response_data = obj_note.update_note(data)
        return response_data

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