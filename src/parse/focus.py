"""Module for the first step of text processing, which is reducing,
a.k.a 'focusing' on the kernel parameter lines themselves"""
import re
from typing import List

from src.parse.step import ParseStep, ParseStepSet
from src.parse.records import KernelParameter


class FilterNonIndented(ParseStep):

    def __init__(self) -> None:
        super().__init__(produces_record=False)
        self.indentation = re.compile(r'^\s+')

    def parse(self, input_str) -> str | List[str]:
        list_input = self.input_list(input_str)
        return [line for line in list_input if not self.indentation.match(line)]

    def is_parsable(self, input_str: str | List[str]) -> bool:
        return input_str is not None and input_str != [] and input_str.strip() != ""


class FocusFirstWord(ParseStep):

    def __init__(self) -> None:
        super().__init__(produces_record=False)
        self.first_word = re.compile(r'^([a-zA-Z0-9._\-]+)')

    def parse(self, input_str: str | List[str]) -> str | List[str]:
        list_input = self.input_list(input_str)
        parsed_list = []
        for line in list_input:
            match_obj = self.first_word.match(line)
            if not match_obj:
                raise ValueError(f'Line {line} has no parseable first word by {self.first_word.pattern}')
            parsed_list.append(match_obj.group(1))

        return parsed_list

    def is_parsable(self, input_str: str | List[str]) -> bool:
        list_input = self.input_list(input_str)
        return input_str is not None and all(line[0].isalnum() for line in list_input)


class SeparateModuleAndParamName(ParseStep):

    def __init__(self, module_param_separator: str = ':'):
        super().__init__(produces_record=False)
        self.values_parsed: dict | None = None
        self.separator = module_param_separator

    def parse(self, input_str: str | List[str]) -> str | List[str]:
        list_input = self.input_list(input_str)
        result = []
        for line in list_input:
            if '.' in line:
                module_name, param_name, *_remaining = line.split('.')
                assert len(_remaining) == 0
                result.append((param_name, module_name))
            else:
                result.append((line, 'core'))
        self.values_parsed = result

        return [self.separator.join([comp[1], comp[0]]) for comp in result]

    def as_record(self):
        return [KernelParameter(*pair) for pair in self.values_parsed] if self.values_parsed is not None else None

    def is_parsable(self, _: str | List[str]) -> bool:
        return True


class FocusStepSet(ParseStepSet):
    def __init__(self) -> None:
        self.input_cache = {}
        self.steps: List[ParseStep] = [FilterNonIndented(), FocusFirstWord(), SeparateModuleAndParamName()]

    def reduce(self, input_str: str | List[str]) -> List[str]:
        steps_taken = 0
        aggregate = input_str
        for step in self.steps:
            if step.is_parsable(aggregate):
                steps_taken += 1
                aggregate = step.parse(aggregate)
            else:
                break
        self.input_cache[input_str] = steps_taken
        return aggregate

    def steps_taken(self, input_str: str | List[str]) -> int:
        return self.input_cache.get(input_str, 0)
