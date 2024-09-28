import requests
from factors.base import ScoringFactor

class ContactsChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str) -> int:
        score = 0
        try: 
            socials = ["contact", "kontakt"]
            response = requests.get(url)
            for social in socials:
                if social in response.text.lower():
                    return 100
        except Exception as e:
            if self.debug:
                print(f"Error while checking socials: {str(e)}")
        return int(score)
