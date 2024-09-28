from urllib.parse import urlparse

import pandas as pd

from .base import ScoringFactor


class CertFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        self.bad_domains_list = pd.read_csv(filename, delimiter="\t")[col].tolist()

    def score(self, url: str, content: str = "") -> int:
        cleaned = urlparse(url).netloc
        return cleaned in self.bad_domains_list
