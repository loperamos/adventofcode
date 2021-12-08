import logging
from collections import Counter, defaultdict, deque
from typing import Generator

from utils.debugging import d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    fishes = deque([0 for _ in range(9)])
    for fish in prob_input.__next__().split(','):
        fishes[int(fish)] += 1
    d(f"{fishes=}")
    for _ in range(80):
        fishes.rotate(-1)
        fishes[6] += fishes[8]
    return sum(fishes)


def pt_2(prob_input: Generator) -> int:
    fishes = deque([0 for _ in range(9)])
    for fish in prob_input.__next__().split(','):
        fishes[int(fish)] += 1
    d(f"{fishes=}")
    for _ in range(256):
        fishes.rotate(-1)
        fishes[6] += fishes[8]
    return sum(fishes)


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
