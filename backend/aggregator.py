import multiprocessing
from os import getpid
from typing import Sequence, Tuple
from urllib.parse import urlparse

from factors.base import ScoringFactor

BASE_SCORE = 100


class URLException(Exception):
    pass


def check_url(url: str) -> (bool, str):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        return False, "URL does not start with 'http://' or 'https://'"
    if not parsed_url.netloc:
        return False, "URL is missing a domain"
    return True, "URL format is valid"


def worker(queue, factor, url, content, weight):
    try:
        score, notes = factor.score(url, content)
    except Exception as exc:
        print(getpid(), exc)
    ret = queue.get()
    ret[getpid()] = [score * weight, notes]
    queue.put(ret)


class ScoreAggregator:
    def __init__(self, debug: bool = True):
        self.debug: bool = debug
        self.factors: Sequence[Tuple[ScoringFactor, float]] = []

    def add_factor(self, factor: ScoringFactor, weight: float) -> None:
        if self.debug:
            print(f"Adding scoring factor: {factor.__class__.__name__}")
        self.factors.append((factor, weight))

    def check_url(self, url: str, content: str = "") -> tuple[int, list[str]]:
        valid, reason = check_url(url)
        if not valid:
            raise URLException(f"Invalid URL: {reason}")

        ret = {}
        queue = multiprocessing.Queue()
        queue.put(ret)
        processes = [
            multiprocessing.Process(
                target=worker, args=(queue, factor, url, content, weight)
            )
            for factor, weight in self.factors
        ]
        [p.start() for p in processes]
        [p.join() for p in processes]
        q = queue.get()
        aggregate = sum([x[0] for x in q.values()])
        aggregate_notes = [item for row in [x[1] for x in q.values()] for item in row]
        return aggregate + BASE_SCORE, aggregate_notes
