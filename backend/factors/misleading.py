from urllib.parse import urlparse
from warnings import catch_warnings

import pandas as pd

from .base import ScoringFactor


class MisleadingSubdomainFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        print(f"Misleading subdomain factor loaded: {filename} {col}")
        self.domains = pd.read_csv(filename)[col].tolist()

    def score(self, url: str, content: str = "") -> int:
        try:
            cleaned = urlparse(url).netloc
            if len(cleaned.split(".")) == 1:
                return 0

            for domain in self.domains:
                domain_name = domain.split(".")[0]
                if cleaned.startswith(domain_name + ".") and not cleaned.endswith(domain):
                    print(
                        f"Analyzed domain {cleaned} has {domain_name} in it but doesn't end with {domain}"
                    )
                    return 1
        except Exception as e:
            print(f"Error while checking misleading subdomain: {str(e)}")
        return 0
