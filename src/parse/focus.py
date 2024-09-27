"""Module for the first step of text processing, which is reducing,
a.k.a 'focusing' on the kernel parameter lines themselves"""

from src.parse.step import ParseStep, ParseStepSet
from pyparsing import Char, Optional, Word, White, LineStart, alphanums
from typing import List
from itertools import chain

class FilterNonIndented(ParseStep):
    
    def __init__(self) -> None:
        self.indentation = LineStart() + White()
        
    def parse(self, input) -> str | List[str]:
        list_input = self.input_list(input)
        return [ line for line in list_input if not self.indentation.parse_string(line)]
    
    def is_parsable(self, input: str | List[str]) -> bool:
        return input != None or input != [] or input.strip() != ""
    
class FocusFirstWord(ParseStep):
    def __init__(self) -> None:
        self.first_word = Word(alphanums + ['_', '.'])
        
    def parse(self, input: str | List[str]) -> str | List[str]:
        list_input = self.input_list(input)
        parsed_double_list = [ self.first_word.parse_string(line).as_list() for line in list_input ]
        return chain.from_iterable(parsed_double_list) # Flatten to single list
        
    def is_parsable(self, input: str | List[str]) -> bool:
        list_input = self.input_list(input)
        return all(line[0].is_alnum() for line in list_input)
    
class SeparateModuleAndParamName(ParseStep):
    def parse(self, input: str | List[str]) -> str | List[str]:
        list_input = self.input_list(input)
        result = []
        for line in list_input:
            if '.' in line:
                dot_index = line.index('.')
                module_name = line[:dot_index]
                param_name = line[dot_index + 1:]
                result.append((module_name, param_name))
            else:
                result.append(('core', line))
                
        return [ f'{comp[0]} - {comp[1]}' for comp in result]
                
    
    def is_parsable(self, input: str | List[str]) -> bool:
        return True

class FocusStepSet(ParseStepSet):
    def __init__(self) -> None:
        self.input_cache = dict()
        self.steps: List[ParseStep] = [FilterNonIndented(), FocusFirstWord(), SeparateModuleAndParamName()]

    def reduce(self, input: str | List[str]) -> List[str]:
        steps_taken = 0
        aggregate = input
        for step in self.steps:
            if step.is_parsable(aggregate):
                steps_taken += 1
                aggregate = step.parse(aggregate)
            else:
                break
        self.input_cache[input] = steps_taken
        return aggregate
    
    @property
    def steps_taken(self, input: str | List[str]) -> int:
        return self.input_cache.get(input, 0)
