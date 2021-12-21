import logging
from itertools import product
from typing import Generator, Any

import numpy as np
from numpy.typing import NDArray

from utils.debugging import debug, info
from utils.runner import run_main

logger = logging.getLogger(__name__)


def get_n(point: NDArray[np.int_]) -> NDArray[np.int_]:
    for i, j in product([-1, 0, 1], [-1, 0, 1]):
        yield point + np.array([i, j])


def print_grid(grid: set[tuple[int, int]]) -> None:
    i_min, i_max, j_min, j_max = get_ranges(grid)
    l = max(i_max - i_min, j_max - j_min)
    img = np.full((l, l), '.')
    for idx in product(range(i_min, i_max + 1), range(j_min, j_max)):
        if idx in grid:
            img[idx[0] - i_min, idx[1] - j_min] = "#"
    for line in img:
        debug(" ".join(line))


def get_ranges(grid: set[[int, int]]) -> [int, int, int, int]:
    i = sorted(grid, key=lambda x: x[0])
    j = sorted(grid, key=lambda x: x[1])
    i_min, i_max, j_min, j_max = i[0][0], i[-1][0] + 1, j[0][1], j[-1][1] + 1
    # debug(f"({i_min}, {i_max}), ({j_min}, {j_max})")
    return i_min, i_max, j_min, j_max


def in_bounds(point: NDArray[np.int_], ranges: [int, int, int, int]) -> bool:
    i_min, i_max, j_min, j_max = ranges
    if point[0] < i_min or point[0] >= i_max:
        return False
    if point[1] < j_min or point[1] >= j_max:
        return False
    return True


def enhance(img: set[[int, int]], enhancement: str, outer: str, ranges: [int, int, int, int]):
    new_img = img.copy()
    i_min, i_max, j_min, j_max = ranges

    for idx in product(range(i_min - 1, i_max + 1), range(j_min - 1, j_max + 1)):
        n = list(get_n(np.array(idx)))
        bin_num = ""
        for p in n:
            if not in_bounds(p, ranges):
                bin_num += "1" if outer == "#" else "0"
            elif tuple(p) in img:
                bin_num += "1"
            else:
                bin_num += "0"

        int_num = int(bin_num, 2)
        light = enhancement[int_num]
        if light == "#":
            new_img.add(idx)
        elif idx in img:
            new_img.remove(idx)
    return new_img


def get_input(prob_input: Generator[str, Any, None]) -> [set[[int, int]], str]:
    enhancement = ""
    for line in prob_input:
        if line == "":
            break
        enhancement += line

    grid = set()
    for i, line in enumerate(prob_input):
        for j, c in enumerate(line):
            if c == "#":
                grid.add((i, j))
    debug(enhancement)
    debug("\n")
    print_grid(grid)
    return grid, enhancement


def increase_ranges(ranges: [int, int, int, int]):
    i_min, i_max, j_min, j_max = ranges
    return i_min - 1, i_max + 1, j_min - 1, j_max + 1


def enhance_many(grid: set[[int, int]], enhancement: str, times: int) -> int:
    outer = '.'
    ranges = get_ranges(grid)
    for i in range(times):
        grid = enhance(grid, enhancement, outer, ranges)
        outer = enhancement[0] if outer == '.' else enhancement[-1]
        ranges = increase_ranges(ranges)

    return len(grid)


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    grid, enhancement = get_input(prob_input)
    return enhance_many(grid, enhancement, 2)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    grid, enhancement = get_input(prob_input)
    return enhance_many(grid, enhancement, 50)


def main():
    run_main(pt_1, pt_2, __file__, [35, 5819, 3351, 18516], run_ex=True)


if __name__ == "__main__":
    main()
