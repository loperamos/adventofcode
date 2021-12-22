import logging
import re
from itertools import product
from typing import Generator, Any

import numpy as np

from utils.debugging import debug
from utils.runner import run_main

logger = logging.getLogger(__name__)

re_line = re.compile(r'^(\w+) x=([\d-]+)\.\.([\d-]+),y=([\d-]+)\.\.([\d-]+),z=([\d-]*)\.\.([\d-]*)$')


def get_instruction(line):
    match = re_line.match(line)
    on_off = match.group(1)
    x = int(match.group(2)), int(match.group(3)) + 1
    y = int(match.group(4)), int(match.group(5)) + 1
    z = int(match.group(6)), int(match.group(7)) + 1
    return on_off == 'on', x, y, z


def range_in_bounds(x_range, y_range, z_range, bounds=50):
    if x_range[0] > bounds or x_range[1] < -bounds:
        return False
    if y_range[0] > bounds or y_range[1] < -bounds:
        return False
    if z_range[0] > bounds or z_range[1] < -bounds:
        return False
    return True


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    grid_on = set()

    for line in prob_input:
        on, x_range, y_range, z_range = get_instruction(line)
        if not range_in_bounds(x_range, y_range, z_range):
            continue
        for p in product(range(*x_range), range(*y_range), range(*z_range)):
            if on:
                grid_on.add(p)
            elif p in grid_on:
                grid_on.remove(p)
    return len(grid_on)

class IntersectFinder:
    memo = {}
    ranges = {}
    def __init__(self, ranges):
        self.ranges = ranges

    def size(self, ranges: list[int]) -> int:



        x_min = max(r[0][0] for r in ranges)
        x_max = min(r[0][1] for r in ranges)

        y_min = max(r[1][0] for r in ranges)
        y_max = min(r[1][1] for r in ranges)

        z_min = max(r[2][0] for r in ranges)
        z_max = min(r[2][1] for r in ranges)

        return (x_max - x_min) * (y_max - y_min) * (z_max - z_min)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    grid_on = set()
    dims = [0, 0, 0]
    edge = [0, 0, 0]

    instructions = list(get_instruction(line) for line in prob_input)

    on = 0


    for _, x_range, y_range, z_range in instructions:




        # dims[0] = max(dims[0], x_range[1] - x_range[0])
        # dims[1] = max(dims[1], y_range[1] - y_range[0])
        # dims[2] = max(dims[2], z_range[1] - z_range[0])
        #
        # edge[0] = min(edge[0], x_range[0])
        # edge[1] = min(edge[1], y_range[0])
        # edge[2] = min(edge[2], z_range[0])

    # debug(f"{dims=}, {edge=}")
    # grid = np.zeros(dims)
    # debug(f"{grid.shape}")


def main():
    run_main(pt_1, pt_2, __file__, [
        0,
        0,
        0,
        0
    ])


if __name__ == "__main__":
    main()
