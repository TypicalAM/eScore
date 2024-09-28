import requests
from factors.base import ScoringFactor

class RobotsDetector(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str) -> int:
        score = 0
        try: 
            response = requests.get(url + "robots.txt")
            if response.status_code == 200:
                score += 50
            else: 
                return score
            for line in response.text.split("\n"):
                if "Sitemap:" in line:
                    site_map_url = line.split(" ")[1]
                    if requests.get(site_map_url).status_code == 200:
                        score += 50
        except Exception as e:
            if self.debug:
                print(f"Error while checking robots.txt: {str(e)}")
        return score
