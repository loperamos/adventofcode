import logging
import sys
from typing import Generator, Any

import numpy as np
from numpy.typing import NDArray
from sortedcontainers import SortedSet

from utils.debugging import debug
from utils.geometry import Grid, Point
from utils.runner import run_main

logger = logging.getLogger(__name__)
MAX_INT = 10000000


def increase_vals(in_array: NDArray, val: int) -> NDArray:
    out = in_array + val
    out[out > 9] -= 9
    return out


def print_array(arr: NDArray) -> None:
    print("\n" + np.array2string(arr, max_line_width=100000))


def get_min_cost(grid: Grid) -> int:
    # print_array(grid.vals)
    distances = Grid(grid.dims, np.full(grid.dims, MAX_INT, dtype=np.dtype))
    distances[Point(0, 0)] = 0
    to_check = SortedSet([(0, Point(0, 0))])
    while len(to_check) != 0:
        dist, point = to_check.pop(0)

        for n in grid.get_neighbours(point, diag=False):
            old_cost = distances[n]
            new_cost = grid[n] + dist
            if new_cost < old_cost:
                if (old_cost, n) in to_check:
                    to_check.remove((old_cost, n))
                distances[n] = new_cost
                to_check.add((new_cost, n))
    # print_array(distances.vals)
    val = distances[Point(grid.dims[0] - 1, grid.dims[1] - 1)]
    return val


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    grid = Grid.from_str(prob_input)
    return get_min_cost(grid)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    grid_tile = Grid.from_str(prob_input)
    tmp_arrays = [np.concatenate(list(increase_vals(grid_tile.vals, i + j) for i in range(5)), axis=0) for j in range(5)]
    grid = Grid.from_arr(np.concatenate(tmp_arrays, axis=1))
    return get_min_cost(grid)


def main():
    run_main(pt_1, pt_2, __file__, [
        40,
        386,
        315,
        2806
    ])


if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    main()
