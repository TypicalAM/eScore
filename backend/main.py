import os
from http import HTTPStatus

from flask import Flask, jsonify, request

from aggregator import ScoreAggregator, URLException

DEBUG = os.getenv('HACKYEAH2024_DEBUG', False) == 'True'
HOST = os.environ.get("HACKYEAH2024_HOST", "0.0.0.0")
PORT = os.environ.get("HACKYEAH2024_PORT", 5000)

aggregator = ScoreAggregator()
app = Flask(__name__)


@app.route("/check_url", methods=["POST"])
def home():
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "No URL provided"}), HTTPStatus.BAD_REQUEST

    url = data["url"]
    try:
        aggregator.check_url(url)
    except URLException as exc:
        if DEBUG:
            print(f"URL exception occured: {str(exc)}")
        return jsonify({"error": str(exc)}), HTTPStatus.BAD_REQUEST
    except Exception as exc:
        print(f"Random exception occured while scoring the url: {str(exc)}")
        return jsonify({"error": "Unknown error"}), HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
