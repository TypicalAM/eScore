from urllib.parse import urlparse

import pandas as pd

from .base import ScoringFactor


class CertFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        self.bad_domains_list = pd.read_csv(filename, delimiter="\t")[col].tolist()

    def score(self, url: str, content: str = "") -> int:
        try: 
            cleaned = urlparse(url).netloc
            return cleaned in self.bad_domains_list
        except Exception as e:
            print(f"Error while checking certificate: {str(e)}")    
        return 0
