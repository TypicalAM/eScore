from typing import Sequence, Tuple

import requests

from factors.base import ScoringFactor


class URLException(Exception):
    pass


def check_url(url: str) -> (bool, str):
    try:
        if not url.startswith(("http://", "https://")):
            return False, "not 'http://' or 'https://'"

        response = requests.head(url, timeout=5)
        if response.status_code >= 200 and response.status_code < 400:
            return True, f"URL is valid. Status Code: {response.status_code}"
        else:
            return False, f"head returned: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return False, f"requests error: {str(e)}"


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
