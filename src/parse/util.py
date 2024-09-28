"""Module for generic utilities used by mostly by parsing backend"""
from itertools import groupby
from typing import Dict


def group_values(values: Dict[str, str]):
    grouping = groupby(values.items(), lambda pair: pair[0])
    return dict(grouping)
