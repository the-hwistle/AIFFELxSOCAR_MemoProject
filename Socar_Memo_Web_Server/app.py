from flask import Flask, redirect, url_for, request, render_template, session
import requests
import json
from operator import itemgetter

app = Flask(__name__)

rest_url = "http://34.132.153.232:5000/"


@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if request.method == "POST":
        description = request.form["description"]
        return render_template("home.html", description=data)

    return render_template("home.html", description=data)


@app.route("/word", methods=["POST"])
def word():
    if request.method == "POST":
        data = request.get_json()
        word = data["word"]
        res = requests.get(f"{rest_url}vocab/search?word={word}")
        data = res.content.decode("unicode-escape")

        if data == None or data == "":
            return None
        data = json.loads(data)
        result = {}
        for d in data:
            result[d[0]] = d[1]
    return result


@app.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":
        data = request.get_json()
        description = data["description"]
        res = requests.get(f"{rest_url}classify?desc={description}")
        data = res.content.decode("unicode-escape")
        if data == None or data == "":
            return None
        data = json.loads(data)
        data = sum(data, [])
    return {"result": data}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
