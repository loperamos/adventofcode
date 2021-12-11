import logging
import statistics
import sys
from typing import Generator

from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    positions = [int(i) for i in prob_input.__next__().split(',')]
    median = statistics.median(positions)
    return int(sum(abs(median - p) for p in positions))


def pt_2(prob_input: Generator) -> int:
    positions = [int(i) for i in prob_input.__next__().split(',')]
    min_cost = int(sys.maxsize)
    for option in range(max(positions)):
        cost = int(sum(abs(p - option) * (abs(p - option) + 1) / 2 for p in positions))
        min_cost = min(cost, min_cost)
    return min_cost


def main():
    run_main(pt_1, pt_2, __file__, [
        37,
        323647,
        168,
        87640209
    ])


if __name__ == "__main__":
    main()
