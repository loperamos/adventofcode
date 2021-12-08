import logging
import statistics
import sys
from typing import *

from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    positions = [int(i) for i in prob_input.__next__().split(',')]
    median = statistics.median(positions)
    return sum(abs(median - p) for p in positions)


def pt_2(prob_input: Generator) -> int:
    positions = [int(i) for i in prob_input.__next__().split(',')]
    min_cost = sys.maxsize
    for option in range(max(positions)):
        cost = sum(abs(p - option) * (abs(p - option) + 1) / 2 for p in positions)
        min_cost = min(cost, min_cost)
    return min_cost


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
