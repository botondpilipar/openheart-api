from abc import ABC, abstractmethod
from typing import List

class ParseStep(ABC):
    @abstractmethod
    def parse(self, input: str | List[str]) -> str | List[str]:
        pass
    
    @abstractmethod
    def is_parsable(self, input: str | List[str]) -> bool:
        pass
    
    def input_list(self, input: str | List[str]):
        return input.splitlines() if isinstance(input, str) else input
    
class ParseStepSet(ABC):
    @abstractmethod
    def reduce(self, input: str | List[str]) -> List[str]:
        pass
    
    @property
    @abstractmethod
    def steps_taken(self, input: str | List[str]) -> int:
        pass
    