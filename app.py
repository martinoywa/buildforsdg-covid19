from flask import Flask, request, jsonify, Response
from src.estimator import estimator
from dicttoxml import dicttoxml

import time
from flask import g

import os
from random import randint

app = Flask(__name__)

app.config["LOGS"] = "logs/"

if "logs" not in os.listdir():
    os.mkdir(app.config["LOGS"])

rand = randint(0, 1000000000)
dir = os.path.join(app.config["LOGS"], "logs"+str(rand)+".txt")

def logger(status):
    now = time.time()
    duration = int((time.time() - g.start) * 1000)
    method = request.method
    path = request.path

    with open(dir, "a") as f:
        f.write(f"{method}\t\t{path}\t\t{status}\t\t{duration} ms\n")


@app.route("/api/v1/on-covid-19/", methods=["GET", "POST"])
@app.route("/api/v1/on-covid-19/json", methods=["GET", "POST"])
def json_index():
    g.start = time.time()

    if request.method == "GET":
        res = Response("", content_type="application/json")
        status = res.status_code
        logger(status)
        return res


    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        res = Response(jsonify(output), content_type="application/json")
        status = res.status_code
        logger(status)
        return jsonify(output)


@app.route("/api/v1/on-covid-19/xml", methods=["GET", "POST"])
def xml_index():
    g.start = time.time()

    if request.method == "GET":
        res = Response("", content_type="application/xml")
        status = res.status[:3]
        logger(status)
        return res

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        res = Response(dicttoxml(output, attr_type=False),  content_type="application/xml")
        status = res.status[:3]
        logger(status)
        return res


@app.route("/api/v1/on-covid-19/logs")
def logs_index():
    with open(dir, "r") as f:
        return Response("".join(f.readlines()), content_type="application/text")


if __name__ == "__main__":
    app.run()
