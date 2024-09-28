import requests

from .base import ScoringFactor


class HSTSFactor(ScoringFactor):
    def score(self, url: str, content) -> int:
        try:
            response = requests.get(url)
            # Check if the Strict-Transport-Security header is present
            if "Strict-Transport-Security" in response.headers:
                print(
                    f"HSTS is enabled for {url}, header: {response.headers['Strict-Transport-Security']}"
                )
                return 0
            return 1
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return 1
