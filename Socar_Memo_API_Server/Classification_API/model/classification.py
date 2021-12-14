import os
from flask_restx import Resource, reqparse
from Classification_API.model.inference import Inferencer
from Classification_API.common.preprocess import Preprocessor

import json


class Predictor:
    def __init__(self) -> None:
        self.preprocessor = Preprocessor()
        self.inferencer = Inferencer()
        self.__call__("타이어")
        print("Initialization_complete")

    def __call__(self, query):
        return self.inferencer.predict(self.preprocessor.run_preprocess(query))


predictor = Predictor()


class Classification(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "desc", required=True, type=str, help="desc cannot be blank"
            )
            args = parser.parse_args()

            desc = args["desc"]

            if desc.strip() == "":
                return []

            result = predictor(desc)
            json_result = json.dumps(result, ensure_ascii=False)
            return json.loads(json_result)

        except Exception as e:
            return {"classification error": str(e)}
