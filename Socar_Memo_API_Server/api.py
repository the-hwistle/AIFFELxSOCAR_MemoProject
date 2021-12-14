from flask import Flask
from flask_restx import Resource, Api
from pymongo import MongoClient
from Vocabulary_API.common import db
from Vocabulary_API.common.downloader import Initialize
from Vocabulary_API.model.vocabulary import Vocab
from Vocabulary_API.model.foreign_vocab import Foreign
from Crawling_API.model.crawling import Crawling
from Classification_API.model.classification import Classification
from Vocabulary_API.common.Bigram.control.bigram_vocab import Bigram_Vocab

app = Flask(__name__)

db.init(app)
api = Api(app)

api.add_resource(Initialize, "/init")
api.add_resource(Classification, "/classify")


# add namespace
api.add_namespace(Vocab, "/vocab")
api.add_namespace(Foreign, "/foreign")
api.add_namespace(Crawling, "/crawling")
api.add_namespace(Bigram_Vocab, "/bigram")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
