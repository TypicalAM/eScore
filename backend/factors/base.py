from abc import ABC, abstractmethod


class ScoringFactor(ABC):
    @abstractmethod
    def score(self, url: str, content: str = "") -> int:
        pass
