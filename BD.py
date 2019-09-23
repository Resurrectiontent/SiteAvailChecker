import pymysql
from pymysql.cursors import DictCursor


class DB:
    # credentials
    _USERNAME, _PASSWORD = 'superman', '$uperPwd'
    # name of database
    _DB_NAME = 'users'
    # name of target table
    _TABLE_NAME = 'ids'

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user=self._USERNAME,
                                          password=self._PASSWORD,
                                          db=self._DB_NAME,
                                          cursorclass=DictCursor)

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
        return bool(self.cursor.execute(query))

    def get_user_ids(self):
        query = '''SELECT *
                   FROM {0}'''.format(self._TABLE_NAME)
        self.cursor.execute(query)
        result_table = self.cursor.fetchall()
        return [row['id'] for row in result_table]
