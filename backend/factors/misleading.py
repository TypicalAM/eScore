from urllib.parse import urlparse

import pandas as pd

from .base import ScoringFactor


class MisleadingSubdomainFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        print(f"Misleading subdomain factor loaded: {filename} {col}")
        self.domains = pd.read_csv(filename)[col].tolist()

    def score(self, url: str) -> int:
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
        return 0
