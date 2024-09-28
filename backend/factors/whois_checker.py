from datetime import datetime
from factors.base import ScoringFactor
import requests


class WhoisChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> int:
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
                            score += 100
        except Exception as e:
            if self.debug:
                print(f"Error while checking whois: {str(e)}")
        return int(score)

