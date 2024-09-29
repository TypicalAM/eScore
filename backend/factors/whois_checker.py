from datetime import datetime

import requests

from factors.base import ScoringFactor


class WhoisChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        score = 0
        try:
            response = requests.get("https://who-dat.as93.net/" + url.split("//")[1])
            if response.status_code == 200:
                response_json = response.json()
                if response_json["domain"]["created_date"] is not None:
                    date_raw = response_json["domain"]["created_date"]
                    year = int(date_raw.split(".")[0])
                    now_year = datetime.now().year - 2
                    if year <= now_year:
                        return 100, []
        except Exception as e:
            if self.debug:
                print(f"Error while checking whois: {str(e)}")
            return 0, ["Failed to get WHOIS status"]

        return int(score), ["Domain was created less than two years ago"]
