from urllib.parse import urlparse

import pandas as pd
from Levenshtein import ratio

from .base import ScoringFactor

LEVENSTEIN_THRESHHOLD = 0.85


class SuspiciousNameFactor(ScoringFactor):
    def __init__(self, filename: str, col: str) -> None:
        print(f"Suspicious name factor loaded: {filename} {col}")
        self.domains = pd.read_csv(filename)[col].tolist()

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        try:
            cleaned = urlparse(url).netloc
            last_name = cleaned.split(".")[-2]  # bogus.exempel.com -> exempel

            for domain in self.domains:
                valid_last_name = domain.split(".")[0]
                levenstein_ratio = ratio(last_name, valid_last_name)
                similar_length = abs(len(last_name) - len(valid_last_name)) < 2
                if (
                    similar_length
                    and levenstein_ratio != 1
                    and levenstein_ratio > LEVENSTEIN_THRESHHOLD
                ):
                    print(
                        f"Analyzed domain {cleaned} is overly similar to {domain} (ratio: {levenstein_ratio})"
                    )
                    return 1, [f"High name similarity between {cleaned} and {domain}"]
        except Exception as e:
            print(f"Error while checking suspicious name: {str(e)}")
            return 1, ["Failed to check name similarity"]
        return 0, []
