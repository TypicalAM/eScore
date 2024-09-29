import json
import os
from dataclasses import asdict, dataclass
from http import HTTPStatus

import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_caching import Cache
from flask_cors import CORS

from aggregator import ScoreAggregator, URLException
from factors import (
    AbuseIpDatabaseFactor,
    CertFactor,
    ContactsChecker,
    GTMChecker,
    HSTSFactor,
    MailFactor,
    MisleadingSubdomainFactor,
    RobotsDetector,
    SocialDetector,
    SuspiciousNameFactor,
    TrustpilotFactor,
    WhoisChecker,
)

DEBUG = os.getenv("HACKYEAH2024_DEBUG", False) == "True"
HOST = os.environ.get("HACKYEAH2024_HOST", "0.0.0.0")
PORT = os.environ.get("HACKYEAH2024_PORT", 5000)
ABUSE_IP_DB_API_KEY = os.environ["HACKYEAH2024_API_KEY"]

tech_standards = ScoreAggregator(debug=DEBUG)
reviews = ScoreAggregator(debug=DEBUG)
phishing = ScoreAggregator(debug=DEBUG)
social = ScoreAggregator(debug=DEBUG)


@dataclass
class AggregatorScore:
    score: float
    notes: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class Scores:
    aggregators: dict[str, AggregatorScore]
    total_score: float
    real_site: str

    def to_json(self) -> str:
        return json.dumps(asdict(self))


app = Flask(__name__)
CORS(app)
app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)


def make_key():  # POST request caching
    user_data = request.get_json()
    return ",".join([f"{key}={value}" for key, value in user_data.items()])


@app.route("/")
def root():
    return send_from_directory("web", "index.html")


@app.route("/<path:path>")
def send_static(path):
    print(path)
    return send_from_directory("web", path)


@app.route("/check_url", methods=["POST"])
@cache.cached(timeout=300, make_cache_key=make_key)
def check_url():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "No URL provided"}), HTTPStatus.BAD_REQUEST

    url = data["url"]
    response = None
    try:
        response = requests.get(url)
    except Exception as exc:
        if DEBUG:
            print(f"Error while fetching the URL: {str(exc)}")
        return jsonify({"error": "Failed to fetch the URL"}), HTTPStatus.BAD_REQUEST
    count = len(response.history)
    count_score = 0
    if count > 5:
        count_score = -10
    last_url = response.url
    if response.status_code > 300:
        return jsonify({"error": "URL is not reachable"}), HTTPStatus.BAD_REQUEST

    scores = {}
    try:
        for name, aggregator in [
            ("reviews", reviews),
            ("phishing", phishing),
            ("social", social),
            ("tech_standards", tech_standards),
        ]:
            score, notes = aggregator.check_url(last_url, response.text)
            scores[name] = AggregatorScore(score, notes)
        scores["tech_standards"].score += count_score
    except URLException as exc:
        if DEBUG:
            print(f"URL exception occured: {str(exc)}")
        return jsonify({"error": str(exc)}), HTTPStatus.BAD_REQUEST
    except Exception as exc:
        print(f"Random exception occured while scoring the url: {str(exc)}")
        return jsonify({"error": "Unknown error"}), HTTPStatus.INTERNAL_SERVER_ERROR

    scores_values = [x.score for x in scores.values()]
    total_score = sum(scores_values) / len(scores_values)
    final = Scores(scores, total_score, last_url)
    return jsonify(final), HTTPStatus.OK


if __name__ == "__main__":
    tech_standards.add_factor(MailFactor(), -10)  # 0 (good) or 1
    tech_standards.add_factor(HSTSFactor(), -10)  # 0 (good) or 1
    tech_standards.add_factor(GTMChecker(DEBUG), -10)  # 0 (good) or 1
    tech_standards.add_factor(WhoisChecker(DEBUG), -10)  # 0 (good) or 1
    tech_standards.add_factor(RobotsDetector(DEBUG), -10)  # 0 (good) or 1

    social.add_factor(CertFactor("cert.csv", "AdresDomeny"), -50)  # 0 (good) or 1
    social.add_factor(
        AbuseIpDatabaseFactor(ABUSE_IP_DB_API_KEY), -0.5
    )  # 0 (good) to 100
    social.add_factor(SocialDetector(DEBUG), -30)  # 0 (good) or 1
    social.add_factor(ContactsChecker(DEBUG), -30)  # 0 (good) or 1

    phishing.add_factor(
        MisleadingSubdomainFactor("pl.csv", "DomainName"), -1.5
    )  # 0 (good) or 1
    phishing.add_factor(
        MisleadingSubdomainFactor("en.csv", "DomainName"), -1.5
    )  # 0 (good) or 1
    phishing.add_factor(
        SuspiciousNameFactor("pl.csv", "DomainName"), -1.5
    )  # 0 (good) or 1
    phishing.add_factor(
        SuspiciousNameFactor("en.csv", "DomainName"), -1.5
    )  # 0 (good) or 1

    reviews.add_factor(TrustpilotFactor(), -1)  # 0 (good) to 50
    app.run(debug=DEBUG, host=HOST, port=PORT)
