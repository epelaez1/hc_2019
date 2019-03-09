from pymongo import MongoClient
from pymongo.errors import BulkWriteError


class MongoDB(object):
    def __init__(self, db_name):
        # config = {
        #     'user': settings.settings[db_name]['user'],
        #     'password': settings.settings[db_name]['pass'],
        #     'host': settings.settings[db_name]['host'],
        #     'database': settings.settings[db_name]['dbname'],
        #     'port': settings.settings[db_name]['port'],
        #     'replicaset': settings.settings[db_name]['replicaset']
        # }
        self._conn = MongoClient(
            ':'.join(["localhost", "27017"]))
        # if db_name is None:
        #     db_name = config['database']
        # # val_user = self._conn[db_name].authenticate(
        # #     config['user'], config['password'], mechanism='SCRAM-SHA-1')
        # if val_user:
        self._db = self._conn[db_name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._conn.close()

    def __del__(self):
        pass