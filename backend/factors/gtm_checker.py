from factors.base import ScoringFactor
import bs4 as bs
import requests

from factors.base import ScoringFactor


class GTMChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> int:
        score = 0
        if 'googletagmanager.com' in content:
            score = 100
        return score
