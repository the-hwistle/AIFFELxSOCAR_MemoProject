from flask_restx import Resource, Api, Namespace, reqparse
from Vocabulary_API.common import db
from Vocabulary_API.model.vocab_tree import Node
import json


class Unknown_Word:
    def __init__(self):
        self.db = db.get_db()

        try:

            if self.get_unknown_word() == None:
                self.create_unknown_word()
        except:
            self.create_unknown_word()
        finally:
            self.unknown_word = self.get_unknown_word()

    def create_unknown_word(self):
        self.db.create_collection("unknown_word")

    def get_unknown_word(self):
        if "unknown_word" not in self.db.list_collection_names():
            raise Exception("Error: unknown_word does not exist")
            return None

        unknown_word = self.db.unknown_word
        return unknown_word

    def get_all_unknown_word_count(self):
        result = self.unknown_word.find({}).count()
        return result

    def find_all(self):
        result = self.unknown_word.find({}, {"_id": 0})

        if result.count() == 0:
            return []

        result = list(result)
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        return json.loads(json_data)

    def find_unknown_word(self, word):
        result = self.unknown_word.find({"node": word}, {"_id": 0})
        if result.count() == 0:
            return []

        result = list(result)
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        return json.loads(json_data)

    def insert_one_unknown_word(self, data):
        if len(self.find_unknown_word(data["node"])) != 0:
            return None

        return self.unknown_word.insert_one(data)

    def insert_many_unknown_word(self, data: list):
        for i in data:
            if len(self.find_unknown_word(i.node)) == 0:
                self.insert_one_unknown_word(i)

        # return self.unknown_word.insert_many(data)

    def update_many_unknown_word(self, data: list):
        # vocab = get_vocabulary()
        # vocab.insert_many(data)
        pass

    def delete_many_unknown_word(self, data: list):
        pass

    def delete_all(self):
        return self.unknown_word.delete_many({})
