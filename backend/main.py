import os
from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_cors import CORS

from aggregator import ScoreAggregator, URLException
from factors.cert import CertFactor
from factors.mail import MailFactor
from factors.misleading import MisleadingSubdomainFactor
from factors.social_detector import SocialDetector
from factors.suspicious import SuspiciousNameFactor

DEBUG = os.getenv("HACKYEAH2024_DEBUG", False) == "True"
HOST = os.environ.get("HACKYEAH2024_HOST", "0.0.0.0")
PORT = os.environ.get("HACKYEAH2024_PORT", 5000)

aggregator = ScoreAggregator()
app = Flask(__name__)
CORS(app)


@app.route("/check_url", methods=["POST"])
def home():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "No URL provided"}), HTTPStatus.BAD_REQUEST

    url = data["url"]
    try:
        score = aggregator.check_url(url)
    except URLException as exc:
        if DEBUG:
            print(f"URL exception occured: {str(exc)}")
        return jsonify({"error": str(exc)}), HTTPStatus.BAD_REQUEST
    except Exception as exc:
        print(f"Random exception occured while scoring the url: {str(exc)}")
        return jsonify({"error": "Unknown error"}), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify({"score": score}), HTTPStatus.OK


if __name__ == "__main__":
    aggregator.add_factor(MailFactor(), -5)
    aggregator.add_factor(CertFactor("cert.csv", "AdresDomeny"), -50)
    aggregator.add_factor(MisleadingSubdomainFactor("en.csv", "DomainName"), -50)
    aggregator.add_factor(MisleadingSubdomainFactor("pl.csv", "DomainName"), -50)
    aggregator.add_factor(SuspiciousNameFactor("en.csv", "DomainName"), -50)
    aggregator.add_factor(SuspiciousNameFactor("pl.csv", "DomainName"), -50)
    aggregator.add_factor(SocialDetector(), 1)
    app.run(debug=DEBUG, host=HOST, port=PORT)
