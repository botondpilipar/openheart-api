"""Module containing abstract classes and interfaces for step-based processing"""
from abc import ABC, abstractmethod
from typing import List


class ParseStep(ABC):

    def __init__(self, produces_record: bool) -> None:
        self.__produces_record = produces_record

    @abstractmethod
    def parse(self, input_str: str | List[str]) -> str | List[str]:
        pass

    @abstractmethod
    def is_parsable(self, input_str: str | List[str]) -> bool:
        pass

    def input_list(self, input_str: str | List[str]):
        return input_str.splitlines() if isinstance(input_str, str) else input_str

    def as_record(self):
        return None

    @property
    def produces_record(self) -> bool:
        return self.__produces_record


class ParseStepSet(ABC):
    @abstractmethod
    def reduce(self, input_str: str | List[str]) -> List[str]:
        pass

    @abstractmethod
    def steps_taken(self, input_str: str | List[str]) -> int:
        pass
