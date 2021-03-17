from abc import ABC, abstractmethod
from typing import List


class AbstractEnvironment(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_info(self) -> List[float]:
        pass

    @abstractmethod
    def act(self, actions: List[float]) -> None:
        pass

    @abstractmethod
    def get_score(self) -> float:
        pass

    @abstractmethod
    def done(self) -> bool:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
