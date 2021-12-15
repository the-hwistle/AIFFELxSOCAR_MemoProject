from flask_restx import Resource, Api, Namespace, reqparse, fields
from flask import jsonify
from Vocabulary_API.common import db
from Vocabulary_API.model.unknown_word import Unknown_Word
from Vocabulary_API.model.vocab_tree import Node
from Crawling_API.model import google, naver
from Crawling_API.common import extraction
from operator import itemgetter
from Vocabulary_API.common.Bigram.model.bigram import Bigram
import json
import os

Vocab = Namespace(name="Vocab", description="Vocabulary 이용하기 위한 API")

# Temp : 단어 토큰화 정보를 위한 파일 로딩
combos_path = os.path.join(os.getcwd(), "data/combos_4000.txt")
f = open(combos_path, encoding="utf8")
lines = f.read().splitlines()
f.close()

temp = [l.split(",") for l in lines]

combo_dict = {}
for t in temp:
    word = t[0]
    token = []
    for i in t[1:]:
        if word == i:
            continue
        token += i.split("/")
    token = [to for to in token if len(to) > 1]
    combo_dict[t[0]] = list(set(token))


@Vocab.route("/search", endpoint="search")
class Search(Resource):
    def get(self):
        try:
            self.vocabulary = Vocabulary()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "word", required=True, type=str, help="word cannot be blank"
            )
            args = parser.parse_args()
            word = args["word"]
            find_result = self.vocabulary.find_start_with_vocabulary(word)
            if isinstance(find_result, list):
                recommendation = {r["node"]: 9999 for r in find_result}
                if len(find_result) < 3:
                    subword = []
                    for fr in find_result:
                        subword += fr["neighbors"]

                    for sub in subword:
                        recommendation[sub["node"]] = sub["weight"]
                recommendation = sorted(
                    recommendation.items(), key=lambda kv: kv[1], reverse=True
                )
                return recommendation

            if isinstance(find_result, str):
                # 단어 유사도 계산 후 출력
                bg_word = Bigram(word)
                words = self.vocabulary.find_query({"bg": {"$in": bg_word.bg}})
                recommendation = []
                for w in words:
                    similarity = len([m for m in bg_word.bg if m in w["bg"]]) / len(
                        w["bg"]
                    )

                    if similarity >= 0.8:
                        recommendation.append((w["node"], similarity))
                        # recommendation[w["node"]] = similarity

                if len(recommendation) < 2:
                    # unknown Word 추가
                    self.unknown_Word = Unknown_Word()
                    word = Node(word)
                    self.unknown_Word.insert_one_unknown_word(word)

                return recommendation

        except Exception as e:
            self.unknown_Word = Unknown_Word()
            word = Node(args["word"])
            self.unknown_Word.insert_one_unknown_word(word)

            return ""


@Vocab.route("/upsert", endpoint="upsert")
class Upsert(Resource):
    def get(self):
        try:
            self.vocabulary = Vocabulary()
            parser = reqparse.RequestParser()
            parser.add_argument(
                "word", required=True, type=str, help="word cannot be blank"
            )
            parser.add_argument("neighbors", required=False)
            parser.add_argument("weights", required=False)
            args = parser.parse_args()

            word = args["word"]
            node = Node(word)
            if "neighbors" in args and "weights" not in args:
                neighbors = args["neighbors"].split(",")
                for n in neighbors:
                    node.add_neighbors(n.strip())
            elif "neighbors" in args and "weights" in args:
                neighbors = args["neighbors"].split(",")
                weights = args["weights"].split(",")
                if len(neighbors) != len(weights):
                    raise Exception("not match neighbors and weights")

                for n, w in zip(neighbors, weights):
                    w = w.strip()
                    try:
                        weight = int(w)
                    except:
                        weight = 0

                    node.add_neighbors(n.strip(), weight)

            result = self.vocabulary.replace_vocabulary_query(
                node["node"], {"neighbors": node.neighbors, "bg": node.bg}
            )
            return result
        except Exception as e:
            return e


@Vocab.route("/update")
class Update(Resource):
    def get(self):
        try:
            self.unknown_word = Unknown_Word()
            self.vocabulary = Vocabulary()
            unknown_list = self.unknown_word.find_all()
            known_list = self.vocabulary.find_all()
            known_list = [known["node"] for known in known_list]
            nouns_dict = self.get_current_corpus_word()
            update_dics = []
            google_crawler = google.Google_Crawler()
            naver_crawler = naver.Naver_Crawler()
            # 검색 및 neighborhood 추가
            for unknown in unknown_list:
                insert_word = []
                unknown_word = unknown["node"]

                insert_word = google_crawler.search(unknown_word)
                insert_word += naver_crawler.search(unknown_word)

                result_ex = extraction.noun_extractor(insert_word)

                node = Node(unknown_word)

                for ex in result_ex:
                    if ex[0] in nouns_dict + known_list:
                        node.add_neighbors(ex[0], ex[1].frequency)

                update_dics.append(node)

                self.vocabulary.insert_many_vocabulary(update_dics)
                self.unknown_word.delete_all()

            return update_dics

        except Exception as e:
            return {"error": str(e)}

    def get_current_corpus_word(self):
        path = os.path.join(os.getcwd(), "data/nouns.txt")
        nouns_set = []
        with open(path, "r") as f:
            for i in f.readlines():
                temp = i.replace(" ", "")
                nouns_set.append(temp.strip())

        return nouns_set

    def create_Node(self, word):
        node = Node(text.strip())
        node.add_neighbors(maker)
        result.append(node)


@Vocab.route("/bigram/update")
class Bigram_Update(Resource):
    def get(self):
        try:
            self.vocabulary = Vocabulary()
            datas = self.vocabulary.find_all()
            for node in datas:
                bi = Bigram(node["node"])
                self.vocabulary.replace_vocabulary_query(node["node"], {"bg": bi.bg})
        except Exception as e:
            return f"{e}"


class Vocabulary:
    def __init__(self):
        self.db = db.get_db()
        if self.get_vocabulary() == None:
            self.create_vocabulary()

        self.vocab = self.get_vocabulary()

    def create_vocabulary(self):
        self.db.create_collection("vocabulary")

    def get_vocabulary(self):
        if "vocabulary" not in self.db.list_collection_names():
            raise Exception("Error: vocabulary does not exist")
            return None

        vocab = self.db.vocabulary
        return vocab

    def get_all_vocabulary_count(self):
        result = self.vocab.find({}).count()
        return result

    def find_all(self):
        result = self.vocab.find({}, {"_id": 0})

        if result.count() == 0:
            return []

        result = list(result)
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        return json.loads(json_data)

    def find_vocabulary(self, word):
        result = self.vocab.find({"node": word}, {"_id": 0})
        if result.count() == 0:
            return []

        # result = [r["node"].encode("utf-8") for r in result]

        result = list(result)
        return result

    def find_query(self, query):
        result = self.vocab.find(query, {"_id": 0})
        result = list(result)
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        return json.loads(json_data)

    def find_start_with_vocabulary(self, word):
        result = self.vocab.find({"node": {"$regex": f"^{word}"}}, {"_id": 0})
        if result.count() == 0:
            return word

        result = list(result)
        json_data = json.dumps(result, ensure_ascii=False, indent=4)
        return json.loads(json_data)

    def insert_many_vocabulary(self, data: list):
        for i in data:
            if len(self.find_vocabulary(i.node)) > 0:
                self.replace_vocabulary_query(
                    i["node"], {"neighbors": i.neighbors, "bg": i.bg}
                )
            else:
                self.insert_one_vocabulary(i)

    def insert_one_vocabulary(self, data):
        data = json.dumps(data)
        data = json.loads(data)
        return self.vocab.insert_one(data)

    def replace_vocabulary(self, data):
        self.vocab.update_one(
            {"node": data.node},
            {"$set": {"neighbors": data.neighbors, "bg": data.bg}},
            upsert=True,
        )

    def replace_vocabulary_query(self, node, query):
        self.vocab.update_one({"node": node}, {"$set": query}, upsert=True)

    def delete_many_vocabulary(self, data: list):
        pass
