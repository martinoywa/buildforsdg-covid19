# Challenge 5
import logging
import time

from flask import Flask, request, g, jsonify, Response
from src.estimator import estimator
from dicttoxml import dicttoxml


app = Flask(__name__)
# initialise log save file
logging.basicConfig(filename="logs.txt", level=logging.INFO)


@app.before_request
def get_time():
    """
        Get time before request
    """
    g.start = time.time()


@app.route("/api/v1/on-covid-19/", methods=["GET", "POST"])
@app.route("/api/v1/on-covid-19/json", methods=["GET", "POST"])
def json_index():
    """
        Handles JSON
    """
    if request.method == "GET":
        res = Response("", content_type="application/json")
        return res, 200

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        return jsonify(output), 200


@app.route("/api/v1/on-covid-19/xml", methods=["GET", "POST"])
def xml_index():
    """
        Handles XML
    """
    if request.method == "GET":
        res = Response("", content_type="application/xml")
        return res, 200

    if request.method == "POST":
        data = request.get_json()
        output = estimator(data)
        res = \
            Response(dicttoxml(
                output, attr_type=False),
                content_type="application/xml")
        return res, 200


@app.route("/api/v1/on-covid-19/logs", methods=["GET", "POST"])
def logs_index():
    """
        Handles Logging
    """
    if request.method != "GET":
        return jsonify({"error": "Method not arrowed"}), 405

    data_logs = []  # logging list
    with open("logs.txt", "rt") as f:   # read logs file and take cycles
        data = f.readlines()
    for line in data:
        if "root" in line and "404" not in line:
            data_logs.append(line[10:])

    return Response("".join(data_logs), mimetype="text/plain")


@app.after_request
def log_request_info(response):
    """
        Gets response as input and returns the logging
        details.
    """
    difference = int((time.time() - g.start) * 1000)
    status_code = response.status.split()[0]
    logging.info(
        f"{request.method}\t\t{request.path}\t\t{status_code}\t\t{str(difference).zfill(2)}ms\n"
    )

    return response


if __name__ == "__main__":
    app.run(debug=True)
