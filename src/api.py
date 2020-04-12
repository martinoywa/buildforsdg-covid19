from flask import Flask


app = Flask(__name__)


@app.route("/api/v1/on-covid-19")
@app.route("/api/v1/on-covid-19/json")
def json_index():
    return "JSON working"


@app.route("/api/v1/on-covid-19/xml")
def xml_index():
    return "XML working"


if __name__ == '__main__':
    app.run(debug=True)
