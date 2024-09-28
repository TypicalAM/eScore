import os
from http import HTTPStatus

import requests
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS

from aggregator import ScoreAggregator, URLException
from factors.abuse_ip_db import AbuseIpDatabaseFactor
from factors.cert import CertFactor
from factors.contacts import ContactsChecker
from factors.gtm_checker import GTMChecker
from factors.hsts import HSTSFactor
from factors.mail import MailFactor
from factors.misleading import MisleadingSubdomainFactor
from factors.robots_detector import RobotsDetector
from factors.social_detector import SocialDetector
from factors.suspicious import SuspiciousNameFactor
from factors.trustpilot import TrustpilotFactor
from factors.whois_checker import WhoisChecker

DEBUG = os.getenv("HACKYEAH2024_DEBUG", False) == "True"
HOST = os.environ.get("HACKYEAH2024_HOST", "0.0.0.0")
PORT = os.environ.get("HACKYEAH2024_PORT", 5000)
ABUSE_IP_DB_API_KEY = os.environ["HACKYEAH2024_API_KEY"]

aggregator = ScoreAggregator(debug=DEBUG)
app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)


@app.route("/check_url", methods=["POST"])
@cache.cached(timeout=300)
def home():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "No URL provided"}), HTTPStatus.BAD_REQUEST

    url = data["url"]
    response = requests.get(url)
    count = len(response.history)
    count_score = 0
    if count > 5:
        count_score = -10
    last_url = response.url
    if response.status_code != 200:
        return jsonify({"error": "URL is not reachable"}), HTTPStatus.BAD_REQUEST
    try:
        score = aggregator.check_url(last_url, response.text) + count_score
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
    aggregator.add_factor(SocialDetector(DEBUG), 1),
    aggregator.add_factor(RobotsDetector(DEBUG), 1),
    aggregator.add_factor(GTMChecker(DEBUG), 1),
    aggregator.add_factor(WhoisChecker(DEBUG), 1),
    aggregator.add_factor(ContactsChecker(DEBUG), 1),
    aggregator.add_factor(TrustpilotFactor(), -1)
    aggregator.add_factor(HSTSFactor(), -1)
    aggregator.add_factor(AbuseIpDatabaseFactor(ABUSE_IP_DB_API_KEY), 1)
    app.run(debug=DEBUG, host=HOST, port=PORT)
