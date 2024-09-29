from factors.base import ScoringFactor


class ContactsChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        try:
            socials = ["contact", "kontakt"]
            for social in socials:
                if social in content.lower():
                    return 100, []
        except Exception as e:
            if self.debug:
                print(f"Error while checking socials: {str(e)}")
            return 0, ["Failed to get contact info status"]
        return 0, ["No contact info"]
