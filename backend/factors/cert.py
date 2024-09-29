from urllib.parse import urlparse

import pandas as pd

from .base import ScoringFactor


class CertFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        self.bad_domains_list = pd.read_csv(filename, delimiter="\t")[col].tolist()

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        try:
            cleaned = urlparse(url).netloc
            test = int(cleaned in self.bad_domains_list)
            if test == 1:
                return 1, ["Listed as harmful in the CERT list"]
            return 0, []
        except Exception as e:
            print(f"Error while checking the cert list: {str(e)}")
            return 1, ["Error while checking CERT validity"]
