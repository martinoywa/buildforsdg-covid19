from flask import Flask, request, jsonify
from estimator import estimator


app = Flask(__name__)


@app.route("/api/v1/on-covid-19/", methods=["GET", "POST"])
@app.route("/api/v1/on-covid-19/json", methods=["GET", "POST"])
def json_index():
    if request.method == "GET":
        return jsonify("JSON working")

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)

        return jsonify(output)


@app.route("/api/v1/on-covid-19/xml")
def xml_index():
    return "XML working"


if __name__ == '__main__':
    app.run(debug=True)
