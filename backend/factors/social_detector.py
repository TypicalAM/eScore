from bs4 import BeautifulSoup

from factors.base import ScoringFactor


class SocialDetector(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        print("SocialDetector")
        score = 1
        try:
            socials = ["facebook", "instagram"]
            content = content.lower()
            for social in socials:
                if social in content:
                    score -= 0.5
        except Exception as e:
            if self.debug:
                print(f"Error while checking socials: {str(e)}")
            return 1, ["Failed to check social media presence status"]

        if int(score) == 1:
            return 1, ["No social accounts linked/present"]
        return int(score), []
