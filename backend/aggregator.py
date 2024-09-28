from typing import Sequence, Tuple
from urllib.parse import urlparse

from factors.base import ScoringFactor


class URLException(Exception):
    pass


def check_url(url: str) -> (bool, str):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        return False, "URL does not start with 'http://' or 'https://'"
    if not parsed_url.netloc:
        return False, "URL is missing a domain"
    return True, "URL format is valid"


class ScoreAggregator:
    def __init__(self, debug: bool = True):
        self.debug: bool = debug
        self.factors: Sequence[Tuple[ScoringFactor, float]] = []

    def add_factor(self, factor: ScoringFactor, weight: float) -> None:
        if self.debug:
            print(f"Adding scoring factor: {factor.__class__.__name__}")
        self.factors.append((factor, weight))

    def check_url(self, url: str) -> int:
        valid, reason = check_url(url)
        if not valid:
            raise URLException(f"Invalid URL: {reason}")

        aggregate = 0
        for factor, weight in self.factors:
            aggregate += weight * factor.score(url)
        return aggregate
