from Vocabulary_API.common.kodex import kodex
from flask_restx import Resource, Api, Namespace, reqparse
from Vocabulary_API.common import db
import json

Foreign = Namespace("Foreign")


@Foreign.route("/search")
class Search(Resource):
    def get(self):
        try:
            self.foreign_vocab = ForeignVocab()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "word", required=True, type=str, help="word cannot be blank"
            )
            args = parser.parse_args()
            word = args["word"]
            code = "".join(map(str, kodex(word)))
            result = self.foreign_vocab.find_foregin_vocabulary(code)
            return result

        except Exception as e:
            return f"Error: {e}"


@Foreign.route("/insert", endpoint="insert")
class Insert(Resource):
    def get(self):
        try:
            self.foreign_vocab = ForeignVocab()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "word", required=True, type=str, help="word cannot be blank"
            )
            args = parser.parse_args()
            word = args["word"]
            result = self.foreign_vocab.insert_foreign_word(word)
            return result

        except Exception as e:
            return f"Error: {e}"


class ForeignVocab:
    def __init__(self):
        self.db = db.get_db()
        if self.get_foreign_vocabulary() == None:
            self.create_foreign_vocabulary()

        self.foregin_vocab = self.get_foreign_vocabulary()

    def create_foreign_vocabulary(self):
        self.db["foregin_vocabulary"]

    def get_foreign_vocabulary(self):
        if "foregin_vocabulary" not in self.db.list_collection_names():
            return None

        vocab = self.db.foregin_vocabulary
        return vocab

    def find_foregin_vocabulary(self, code):
        result = self.foregin_vocab.find({"code": code}, {"_id": 0})

        if result.count() == 0:
            return []

        result = list(result)
        return result

    def insert_foreign_word(self, word):
        code = "".join(map(str, kodex(word)))

        if len(self.find_foregin_vocabulary(code)) == 0:
            data = {"code": code, "word": word}
            data = json.dumps(data)
            data = json.loads(data)
            self.foregin_vocab.insert_one(data)

        return ""
