import heapq
import logging
import sys
from typing import Generator, Any

import numpy as np
from numpy.typing import NDArray

from utils.debugging import print_array
from utils.geometry import Grid, Point
from utils.runner import run_main

logger = logging.getLogger(__name__)
MAX_INT = 20000000


def increase_vals(in_array: NDArray, val: int) -> NDArray:
    out = in_array + val
    out[out > 9] -= 9
    return out


def get_min_cost_heap(grid: Grid) -> int:
    print_array(grid.vals)
    distances = Grid(grid.dims, np.full(grid.dims, -1, dtype=int))
    heap = [(0, Point(0, 0))]
    last_pont = Point(grid.dims[0] - 1, grid.dims[1] - 1)
    while heap:
        dist, p = heapq.heappop(heap)
        val = grid[p]

        new_val = dist + val
        if distances[p] == -1 or new_val < distances[p]:
            distances[p] = new_val
        else:
            continue
        if p == last_pont:
            break

        for n in grid.get_neighbours(p, diag=False):
            heapq.heappush(heap, (new_val, n))

    return distances[last_pont] - distances[Point(0, 0)]


def get_min_cost(grid: Grid) -> int:
    print_array(grid.vals)
    distances = Grid(grid.dims, np.full(grid.dims, MAX_INT, dtype=int))
    distances[Point(0, 0)] = 0
    to_check = [(0, Point(0, 0))]
    last_pont = Point(grid.dims[0] - 1, grid.dims[1] - 1)
    while to_check:
        dist, point = heapq.heappop(to_check)
        for n in grid.get_neighbours(point, diag=False):
            old_cost = distances[n]
            new_cost = grid[n] + dist
            if new_cost < old_cost:
                distances[n] = new_cost
                heapq.heappush(to_check, (new_cost, n))
                if n == last_pont:
                    return new_cost
    val = distances[last_pont]
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
    grid = Grid.from_arr(np.array([
        [1, 100, 1, 1, 1, 1],
        [1, 1, 1, 100, 100, 1],
        [100, 100, 1, 2, 1, 1]
    ]))
    print(get_min_cost(grid))
    run_main(pt_1, pt_2, __file__, [
        40,
        386,
        315,
        2806
    ])


if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize, linewidth=10000)
    main()
