from flask import Flask, request, jsonify, Response
from estimator import estimator
from dicttoxml import dicttoxml


app = Flask(__name__)


@app.route("/api/v1/on-covid-19/", methods=["GET", "POST"])
@app.route("/api/v1/on-covid-19/json", methods=["GET", "POST"])
def json_index():
    if request.method == "GET":
        return j

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)

        return jsonify(output)


@app.route("/api/v1/on-covid-19/xml", methods=["GET", "POST"])
def xml_index():
    if request.method == "GET":
        return Response("XML working",  mimetype="text/xml")

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)

        return Response(dicttoxml(output),  mimetype="text/xml")


if __name__ == '__main__':
    app.run(debug=True)
