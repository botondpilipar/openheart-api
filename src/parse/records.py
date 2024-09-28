"""Module containing SQL and non-SQL record definitions"""
from dataclasses import dataclass


@dataclass
class KernelParameter:
    parameter_name: str
    module_name: str = 'core'
