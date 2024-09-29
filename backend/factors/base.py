from abc import ABC, abstractmethod


class ScoringFactor(ABC):
    @abstractmethod
    def score(self, url: str, content: str = "") -> list[int, list[str]]:
        pass
