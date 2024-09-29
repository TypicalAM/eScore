from factors.base import ScoringFactor


class GTMChecker(ScoringFactor):

    def __init__(self, debug: bool = True):
        self.debug: bool = debug

    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        if "googletagmanager.com" not in content:
            return 1, ["Google Tag Manager missing"]
        return 0, []
