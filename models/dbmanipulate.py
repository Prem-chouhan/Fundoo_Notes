import re
from email.mime.text import MIMEText
from config.connection import DbConnect
import os
from config.connection import con

my_db = con

class model:

    def __init__(self):
        pass

    def insert(self, data, table_name):
        table_name = table_name
        column = []
        rows_values = []
        val = []

        for key, value in data.items():
            column.append(key)
            rows_values.append("%s")
            val.append(value)

        column = ', '.join(column)
        val_ = ', '.join(['%s'] * len(val))

        print(column)
        print(rows_values)
        print(val)
        query = '''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, column, val_)
        print(query)

        my_db.queryExecute(query=query, value=val)

    # def insert_user(self, email, password):
    #     """Insert Query is fired Here and registration is done"""
    #     sql = "INSERT INTO user(email,password) VALUES (%s, %s)"
    #     val = (email, password)
    #     my_db.queryExecute(sql, val)

    def read_email(self, email=None, id=None):
        id = None
        """Select Query is fired Here and email address is present or not is shown """
        sql = "SELECT id FROM user where email = '" + email + "'"
        result = my_db.queryfetch(sql)
        print(result)
        # print(result[0][1], "---------re")
        if len(result) > 0:
            print("------Inside")
            id = result[0]
            if id is not None:
                print("qwertyui")
                return id
        return id

    def update_password(self, data, key):
        """Here password is updated with update query"""
        sql = "UPDATE user SET password = '" + data['password'] + "' WHERE email = '" + key + "' "
        my_db.query(sql)

    # def insert(self, data):
    #     """
    #     Insert Query Fired
    #     Fields of table:param data:
    #     no:return:
    #     """
    #     print("inside insert query")
    #     sql = "INSERT INTO notes(tittle,description,color,is_pinned,is_archived,is_trashed,user_id) VALUES (%s,%s,%s," \
    #           "%s,%s,%s, %s) "
    #     val = (
    #         data['tittle'], data['description'], data['color'], data['is_pinned'], data['is_archived'],
    #         data['is_trashed'],
    #         data['user_id'])
    #     my_db.queryExecute(sql, val)

    def update(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        sql = "UPDATE notes SET tittle = '" + data['tittle'] + "' WHERE id = '" + data['id'] + "' "
        my_db.query(sql)

    def delete(self, data):
        """
        Delete query is fired
        id :param data:
        no:return:
        """
        sql = "DELETE FROM notes WHERE id = '" + data['id'] + "'"
        my_db.query(sql)

    def update_profile(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        # print(, type(data['user_id']))
        profile_path = data['profile_path']
        id = data['id']
        print(id)
        sql = "INSERT INTO profile(profile_path,user_id) VALUES (%s, %s)"
        val = (profile_path, id)
        my_db.queryExecute(sql, val)

    def remainders(self):
        sql = "select * from notes where is_pinned = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def archives(self):
        sql = "select * from notes where is_trashed = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def trashed(self):
        sql = "select * from notes where is_archived = 1"
        catch = my_db.queryfetch(sql)
        return catch

