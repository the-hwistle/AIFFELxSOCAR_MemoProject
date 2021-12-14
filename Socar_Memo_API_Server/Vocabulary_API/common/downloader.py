from flask_restx import Resource
from Vocabulary_API.model.vocab_tree import Node, Neighbor
from Vocabulary_API.model.vocabulary import Vocabulary, Unknown_Word
from Crawling_API.model import google, naver
from Crawling_API.common import extraction
from tqdm import tqdm

import os


class Initialize(Resource):
    """
    바로 단어장에 넣는 것이 아닌 대기열에 쌓음
    업데이트를 할 때 기존 베이스 단어들과 비교해서 단어장에 추가

    """

    def __init__(self, *args):
        self.vocab = Vocabulary()
        self.unknown = Unknown_Word()

    def get(self):
        if self.vocab.get_all_vocabulary_count() != 0:
            return

        self.insert_base_word_to_unknownlist()
        self.upgrade_vocabulary()
        self.insert_car_name_to_unknownlist()
        self.upgrade_vocabulary()

        return "init success"

    def insert_base_word_to_unknownlist(self):
        _path = os.path.join(os.getcwd(), "data/nouns_3084.txt")
        data = self.download_from_file(_path)
        result = []
        for d in data:
            node = Node(d.strip())
            result.append(node)

        self.insert_to_unkwnown(result)

    def insert_car_name_to_unknownlist(self):
        _path = os.path.join(os.getcwd(), "data/car_name.txt")
        data = self.download_from_file(_path)
        result = []
        for d in data:
            if d.startswith("="):
                d = d.replace("=", "")
            node = Node(d.strip())
            result.append(node)

        self.insert_to_unkwnown(result)

    def insert_to_unkwnown(self, data):
        self.unknown.insert_many_unknown_word(data)

    def upgrade_vocabulary(self):
        unknown_list = self.unknown.find_all()
        unknown_node_list = [unknown["node"] for unknown in unknown_list]
        known_list = self.vocab.find_all()
        known_node_list = [known["node"] for known in known_list]
        google_crawler = google.Google_Crawler()
        naver_crawler = naver.Naver_Crawler()
        for unknown in tqdm(unknown_node_list):
            insert_word = []
            unknown_word = unknown
            insert_word = google_crawler.search(unknown_word)
            insert_word += naver_crawler.search(unknown_word)
            # insert_word = preprocessing.clean_sentence(insert_word)
            result_ex = extraction.noun_extractor(insert_word)

            node = Node(unknown_word)

            for ex in result_ex:
                if ex[0] in unknown_node_list + known_node_list:
                    node.add_neighbors(ex[0], ex[1].frequency)
            self.vocab.insert_one_vocabulary(node)

        self.unknown.delete_all()

    def download_from_file(self, file_path):
        result = []
        with open(file_path, "r") as f:
            for text in f.readlines():
                result.append(text)

        return result
