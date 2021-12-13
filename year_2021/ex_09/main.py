import logging
import math
from typing import Generator, Any

from utils.debugging import debug
from utils.geometry import Point, Grid
from utils.runner import run_main

logger = logging.getLogger(__name__)


def is_in_board(pos: Point, n: int, m: int) -> bool:
    if pos.i < 0 or pos.i >= n:
        return False
    if pos.j < 0 or pos.j >= m:
        return False
    return True


def get_neighbours(pos: Point, n: int, m: int) -> Generator[Point, Any, None]:
    neighbours = [pos + Point(1, 0), pos + Point(-1, 0), pos + Point(0, 1), pos + Point(0, -1)]
    return (neighbour for neighbour in neighbours if is_in_board(neighbour, n, m))


def pt_1(prob_input: Generator) -> int:
    heightmap = Grid.from_str(prob_input)
    count = 0

    for point, h in heightmap.items():
        local_min = True
        for neighbour in heightmap.get_neighbours(point, diag=False):
            n_h = heightmap[neighbour]
            if h >= n_h:
                local_min = False
        if local_min:
            count += 1 + h
    return count


def pt_2(prob_input: Generator) -> int:
    heightmap = Grid.from_str(prob_input)

    all_idx = set(heightmap.points())
    sizes = []
    while all_idx:
        indexes = [all_idx.pop()]
        current_size = 0
        while indexes:
            to_check = indexes.pop()
            h = heightmap[to_check]
            if h == 9:
                continue
            current_size += 1
            for neighbour in heightmap.get_neighbours(to_check, diag=False):
                if neighbour in all_idx:
                    all_idx.remove(neighbour)
                    indexes.append(neighbour)

        debug(f"{current_size=}")
        if current_size > 0:
            sizes.append(current_size)

    top_3 = sorted(sizes, reverse=True)[:3]
    debug(f"{top_3=}")
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
