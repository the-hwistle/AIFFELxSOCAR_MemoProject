from flask_restx import Resource, Api, Namespace, reqparse
from Crawling_API.model import google, naver
import json

Crawling = Namespace("Crawling")


@Crawling.route("/google")
class GoogleCrawler(Resource):
    def get(self):
        try:

            parser = reqparse.RequestParser()
            parser.add_argument("p", required=True, type=str, help="p cannot be blank")
            args = parser.parse_args()
            p = args["p"]
            google_crawler = google.Google_Crawler()
            search_result = google_crawler.search(p)
            json_result = json.dumps(search_result, ensure_ascii=False)
            return json_result

        except Exception as e:
            return {"error": str(e)}


@Crawling.route("/naver")
class NaverCrawler(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("p", required=True, type=str, help="p cannot be blank")
            args = parser.parse_args()
            p = args["p"]
            naver_crawler = naver.Naver_Crawler()
            search_result = naver_crawler.search(p)
            json_result = json.dumps(search_result, ensure_ascii=False)
            return json_result

        except Exception as e:
            return {"error": str(e)}
