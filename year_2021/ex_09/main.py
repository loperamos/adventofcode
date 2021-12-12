import logging
import math
from typing import Generator, Any

import numpy as np

from utils.debugging import d, df
from utils.runner import run_main
from utils.geometry import Point

logger = logging.getLogger(__name__)


def is_in_board(pos: Point, n: int, m: int) -> bool:
    if pos.i < 0 or pos.i >= n:
        return False
    if pos.j < 0 or pos.j >= m:
        return False
    return True


def get_neighbours(pos: Point, n: int, m: int) -> Generator[Point, Any, None]:
    neighbours = [pos + Point.from_vals(1, 0), pos + Point.from_vals(-1, 0), pos + Point.from_vals(0, 1), pos + Point.from_vals(0, -1)]
    return (neighbour for neighbour in neighbours if is_in_board(neighbour, n, m))


def pt_1(prob_input: Generator) -> int:
    heightmap = np.array([[int(pos) for pos in row] for row in prob_input])
    df(heightmap)

    n = len(heightmap)
    m = len(heightmap[0])

    count = 0

    for i in range(n):
        row = heightmap[i]
        for j in range(m):
            local_min = True
            h = row[j]
            for neighbour in get_neighbours(Point.from_vals(i, j), n, m):
                n_h = heightmap[neighbour.i, neighbour.j]
                if h >= n_h:
                    local_min = False
            if local_min:
                count += 1 + h
    return count


def pt_2(prob_input: Generator) -> int:
    heightmap = np.array([[int(pos) for pos in row] for row in prob_input])
    df(heightmap)

    n = len(heightmap)
    m = len(heightmap[0])

    all_idx = {Point.from_vals(i, j) for j in range(m) for i in range(n)}
    sizes = []
    while all_idx:
        indexes = [all_idx.pop()]
        current_size = 0
        while indexes:
            to_check = indexes.pop()
            h = heightmap[to_check.i, to_check.j]
            if h == 9:
                continue
            current_size += 1
            for neighbour in get_neighbours(to_check, n, m):
                if neighbour in all_idx:
                    all_idx.remove(neighbour)
                    indexes.append(neighbour)

        d(f"{current_size=}")
        if current_size > 0:
            sizes.append(current_size)

    top_3 = sorted(sizes, reverse=True)[:3]
    d(f"{top_3=}")
    return math.prod(top_3)


def main():
    run_main(pt_1, pt_2, __file__, [
        15,
        486,
        1134,
        1059300
    ])


if __name__ == "__main__":
    main()
