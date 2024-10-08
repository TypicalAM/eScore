from urllib.parse import urlparse

import requests
from dns import resolver
from requests.utils import quote

from .base import ScoringFactor

CLOUDFLARE_DNS = "1.1.1.1"
ABUSE_IP_DB_URL = "https://api.abuseipdb.com/api/v2/check"


class AbuseIpDatabaseFactor(ScoringFactor):
    def __init__(self, key: str, dns_server: str = CLOUDFLARE_DNS) -> None:
        self.api_key = key
        self.dns_server = dns_server
        self.resolver = resolver.Resolver()
        self.resolver.nameservers = [
            dns_server,
        ]
        self.headers = {"Key": f"{self.api_key}", "Accept": "application/json"}

    def score(self, url: str, content) -> list[int, list[str]]:
        cleaned = urlparse(url).netloc
        print(f"Sending A DNS query for {cleaned} via {self.dns_server}")
        a = self.resolver.resolve(cleaned, "A")
        for record in a:
            params = {"ipAddress": quote(str(record))}
            resp = requests.get(ABUSE_IP_DB_URL, params=params, headers=self.headers)
            abuse_score = resp.json()["data"]["abuseConfidenceScore"]
            print(
                f"Abuse IP DB reported an abuse score for {str(record)} as {abuse_score}"
            )
            if int(abuse_score) > 50:
                return int(abuse_score), ["High IP abuse score"]
            return int(abuse_score), []
        return 0, ["IP abuse status not present"]
