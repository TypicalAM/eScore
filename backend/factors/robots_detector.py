import requests

from factors.base import ScoringFactor


class RobotsDetector(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        score = 0
        try:
            response = requests.get(url + "/robots.txt")
            if response.status_code == 200:
                score = 0
            else:
                return 1, ["Site doesn't contain robots.txt"]
            for line in response.text.split("\n"):
                if "Sitemap:" in line:
                    site_map_url = line.split(" ")[1]
                    if requests.get(site_map_url).status_code == 200:
                        score = 0
                    else:
                        score = 1
        except Exception as e:
            if self.debug:
                print(f"Error while checking robots.txt: {str(e)}")
            return 1, ["Failed to get robots.txt"]
        if score == 1:
            return 1, ["Site has a valid robots.txt, but sitemap is nonexistent"]
        return score, []
