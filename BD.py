import sqlite3


class DB:
    # name of database
    _DB_NAME = 'users.db'
    # name of target table
    _TABLE_NAME = 'ids'

    def __init__(self):
        self.connection = sqlite3.connect(self._DB_NAME, check_same_thread=False)

        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        if not self._user_exists(user_id):
            query = '''INSERT INTO {0}(id) 
                       VALUES ({1});'''.format(self._TABLE_NAME, user_id)
            if not self.cursor.execute(query):
                return {'type': 'Failure', 'value': 'Error adding user to database.'}
            else:
                self.connection.commit()
                return {'type': 'Success', 'value': 'User added to database.'}
        else:
            return {'type': 'Failure', 'value': 'User already exists.'}

    def remove_user(self, user_id):
        if self._user_exists(user_id):
            query = '''DELETE FROM {0}
                       WHERE id = {1};'''.format(self._TABLE_NAME, user_id)
            if not self.cursor.execute(query):
                return {'type': 'Failure', 'value': "User doesn't exist."}
            else:
                self.connection.commit()
                return {'type': 'Success', 'value': 'User removed from database.'}
        else:
            return {'type': 'Failure', 'value': "User doesn't exist."}

    def _user_exists(self, user_id):
        query = '''SELECT *
                   FROM {0}
                   WHERE id = {1}'''.format(self._TABLE_NAME, user_id)
        self.cursor.execute(query)
        return bool(self.cursor.fetchall())

    def get_user_ids(self):
        query = '''SELECT *
                   FROM {0}'''.format(self._TABLE_NAME)
        self.cursor.execute(query)
        result_table = self.cursor.fetchall()
        return [row[1] for row in result_table]

    def disconnect(self):
        self.connection.commit()
        self.connection.close()
