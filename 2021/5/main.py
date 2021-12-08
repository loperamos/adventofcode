import logging
from collections import defaultdict
from typing import *

import numpy as np
from numpy.typing import NDArray

from utils.debugging import d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def parse_line(line):
    a, b = line.split(' -> ')
    x1, y1 = a.split(',')
    x2, y2 = b.split(',')
    return np.array([int(x1), int(y1)]), np.array([int(x2), int(y2)])


def range_points(start: NDArray[int], stop: NDArray[int]):
    diff = (stop - start).astype(int)
    step = np.array([
        diff[0] / abs(diff[0]) if diff[0] != 0 else 0,
        diff[1] / abs(diff[1]) if diff[1] != 0 else 0,
    ]).astype(int)
    points = abs(diff[0]) if diff[0] != 0 else abs(diff[1])
    return (start + step * i for i in range(points + 1))


def pt_1(prob_input: Generator) -> int:
    counting = defaultdict(int)
    for line in prob_input:
        start, end = parse_line(line)
        if start[0] != end[0] and start[1] != end[1]:
            continue
        for i, j in range_points(start, end):
            counting[(i, j)] += 1
    total = len([i for i in counting.values() if i >= 2])
    return total


def pt_2(prob_input: Generator) -> int:
    counting = defaultdict(int)
    for line in prob_input:
        start, end = parse_line(line)
        for i, j in range_points(start, end):
            counting[(i, j)] += 1
    total = len([i for i in counting.values() if i >= 2])
    return total


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
