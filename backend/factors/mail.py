from urllib.parse import urlparse

from dns import resolver

from .base import ScoringFactor

CLOUDFLARE_DNS = "1.1.1.1"
SPF_DROP_ALL_RULE = "v=spf1 -all"
SPF_MARKER = "v=spf1"
SPF_IP_MARKER = "ip4:"
DMARC_MARKER = "v=DMARC1"
NO_MX_MARKER = "0 ."


class MailFactor(ScoringFactor):
    def __init__(self, dns_server: str = CLOUDFLARE_DNS) -> None:
        self.dns_server = dns_server
        self.resolver = resolver.Resolver()
        self.resolver.nameservers = [
            dns_server,
        ]

    def score(self, url: str, content: str = "") -> int:
        cleaned = urlparse(url).netloc
        mx = []
        txt = []
        try:
            print(f"Sending MX DNS query for {cleaned} via {self.dns_server}")
            mx = self.resolver.resolve(cleaned, "MX")
            print(f"Sending TXT DNS query for {cleaned} via {self.dns_server}")
            txt = self.resolver.resolve(cleaned, "TXT")
        except Exception as exc:
            print(f"Exception while sending DNS queries: {str(exc)}")
            return 1
        if len(mx) == 0 or NO_MX_MARKER in mx[0].to_text():
            for record in txt:
                if SPF_DROP_ALL_RULE in record.to_text():
                    print(f"SPF drop all rule discovered in {cleaned}")
                    return 0
            print(f"SPF drop all rule missing in {cleaned}")
            return (
                1  # If we don't have an MX records we should have an SPF hard drop rule
            )

        spf_found = False
        for record in txt:
            if SPF_MARKER in record.to_text() and SPF_IP_MARKER in record.to_text():
                print(f"SPF rule discovered in {cleaned}")
                spf_found = True
        if not spf_found:
            print(f"SPF ipv4 rule missing in {cleaned}")
            return 1

        dmarc_domain = "_dmarc." + cleaned
        print(f"Sending TXT DNS query for {dmarc_domain} via {self.dns_server}")
        txt = self.resolver.resolve(dmarc_domain, "TXT")
        for record in txt:
            if DMARC_MARKER in record.to_text():
                print(f"DMARC rule discovered in {cleaned}")
                return 0  # All domains with a valid SPF record should also have a valid DMARC
        print(f"DMARC rule discovered in {cleaned}")
        return 1  # All domains with a valid SPF record should also have a valid DMARC
