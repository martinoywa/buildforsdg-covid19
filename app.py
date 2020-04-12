from flask import Flask, request, jsonify, Response
from src.estimator import estimator
from dicttoxml import dicttoxml


app = Flask(__name__)


@app.route("/api/v1/on-covid-19/", methods=["GET", "POST"])
@app.route("/api/v1/on-covid-19/json", methods=["GET", "POST"])
def json_index():
    if request.method == "GET":
        return jsonify("")

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)

        return jsonify(output)


@app.route("/api/v1/on-covid-19/xml", methods=["GET", "POST"])
def xml_index():
    if request.method == "GET":
        return Response("", content_type="application/xml")

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)

        return Response(dicttoxml(output, attr_type=False),  content_type="application/xml")


if __name__ == "__main__":
    app.run()
