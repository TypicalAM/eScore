import requests
from bs4 import BeautifulSoup
from factors.base import ScoringFactor

class SocialDetector(ScoringFactor):

    def score(self, url: str) -> int:
        socials = ["facebook", "instagram"]
        points_per_social = 100 / len(socials)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        links = soup.find_all("a")
        score = 0
        for link in links:
            for social in socials:
                if social in link.get("href"):
                    score += points_per_social
                    socials.remove(social)
        return int(score)
