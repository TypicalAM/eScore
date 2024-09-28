from factors.base import ScoringFactor
import bs4 as bs
import requests

class GTMChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str) -> int:
        score = 0
        response = requests.get(url)
        if response.status_code == 200:
            if 'googletagmanager.com' in response.text:
                score = 100
        return score
