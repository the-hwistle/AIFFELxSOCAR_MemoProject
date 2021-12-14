from flask_restx import Resource, Api, Namespace, reqparse
from flask import jsonify
from Vocabulary_API.common.Bigram.model.bigram import Bigram
from Vocabulary_API.common import db
import json

Bigram_Vocab = Namespace("Bigram_Vocab")


@Bigram_Vocab.route("/download")
class Download(Resource):
    def get(self):
        try:
            pass

        except Exception as e:
            pass
            return ""


@Bigram_Vocab.route("/insert")
class Insert(Resource):
    def get(self):
        try:
            bigram_vocab = Bigram_Vocabulary()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "word", required=True, type=str, help="word cannot be blank"
            )
            args = parser.parse_args()
            word = args["word"]
            bg = Bigram(word)
            bigram_vocab.insert_document(bg)
            return "bigram insert"

        except Exception as e:
            return f"{e}"


class Bigram_Vocabulary:
    def __init__(self):
        self.db = db.get_db()
        if self.get_collection() == None:
            self.create_collection()

        self.bigram = self.get_collection()

    def create_collection(self):
        self.db["bigram"]

    def get_collection(self):
        if "bigram" not in self.db.list_collection_names():
            return None

        vocab = self.db.bigram
        return vocab

    def find_bigram(self, code):
        result = self.bigram.find({"code": code}, {"_id": 0})

        if result.count() == 0:
            return []

        result = list(result)
        return result

    def insert_document(self, word: Bigram):
        data = json.dumps(word)
        data = json.loads(data)
        self.bigram.insert_one(data)
