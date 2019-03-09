from database.mongodb import MongoDB
from core.utils import utils
from pymongo.errors import BulkWriteError
from core.logger import PersonalLogger


class HashCodeDB(MongoDB):

    def __init__(self):
        super().__init__("HashCodeDB")
    def create_index(self, collection, field):
        try:
            return self._db[collection].create_index(
                field)
        except Exception as error:
            utils.print_exception()
    def find_one_and_delete(self, collection:str, mongo_query: dict, sort: list = []):
        try:
            return self._db[collection].find_one_and_delete(mongo_query)
        except Exception as error:
            utils.print_exception()
    def count(self, collection:str):
        try:
            return self._db[collection].count()
        except Exception as error:
            utils.print_exception()
    def search(self, collection: str, mongo_query, fields={}, sort={}, limit=100000000):
        try:
            if fields:
                result = self._db[collection].find(mongo_query, fields, sort=sort, limit=limit)
            else:
                result = self._db[collection].find(mongo_query, sort=sort, limit=limit)
            return result
        except Exception as error:
            utils.print_exception()

    def update(
            self, collection: str,
            mongo_query: dict, set_query: dict,
            multi: bool = False):
        try:
            return self._db[collection].update(
                mongo_query,
                {"$set": set_query},
                multi=multi)
        except Exception as error:
            utils.print_exception()

    def insert_one(self, collection: str, new_element: dict):
        try:
            return self._db[collection].insert_one(new_element)
        except Exception as error:
            utils.print_exception()

    def insert_many(self, collection, new_elements: list):
        try:
            self._db[collection].insert_many(
                new_elements, bypass_document_validation=True)
        except BulkWriteError as bwe:
            utils.print_exception()

    def push(self, collection, mongo_query, push_statement):
        try:
            return self._db[collection].update(
                mongo_query,
                {"$push": push_statement})
        except Exception as error:
            utils.print_exception()

    def drop_collection(self, collection):
        try:
            return self._db[collection].drop()
        except Exception as error:
            utils.print_exception()

    def pull(self, collection, mongo_query, pull_statement, multi: bool = False):
        try:
            return self._db[collection].update(
                mongo_query,
                {"$pull": pull_statement},
                multi = multi)
        except Exception as error:
            utils.print_exception()
    def remove(
            self, collection: str,
            mongo_query: dict,
            multi: bool = False):
        try:
            return self._db[collection].remove(
                mongo_query,
                multi=multi)
        except Exception as error:
            utils.print_exception()