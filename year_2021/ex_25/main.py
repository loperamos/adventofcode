import logging
from typing import Generator, Any

import numpy as np
from sortedcontainers import SortedSet

from utils.debugging import debug, print_array_as_str
from utils.runner import run_main

logger = logging.getLogger(__name__)


def draw(east: list[SortedSet], south: list[SortedSet], dims: [int, int]) -> None:
    mat = np.full(dims, '.')
    for i, row in enumerate(east):
        for j in row:
            mat[i, j] = '>'
    for j, col in enumerate(south):
        for i in col:
            mat[i, j] = 'v'
    print_array_as_str(mat, dbg=False)


def move_east(east: list[SortedSet], south: list[SortedSet], dims: [int, int]) -> bool:
    moved = False
    for i, row in enumerate(east):
        if not row:
            continue
        first = row[0] == 0
        for k in range(len(row)):
            j = row[k]
            if j == dims[1] - 1:
                if first or i in south[0]:
                    continue
                row.remove(j)
                row.add(0)
                moved = True
                continue
            if i in south[j + 1]:
                continue
            if j + 1 not in row:
                row.remove(j)
                row.add(j + 1)
                moved = True
    return moved


def move_south(east: list[SortedSet], south: list[SortedSet], dims: [int, int]) -> bool:
    moved = False
    for j, col in enumerate(south):
        if not col:
            continue
        first = col[0] == 0
        for k in range(len(col)):
            i = col[k]
            if j in east[i]:
                continue
            if i == dims[0] - 1:
                if first or j in east[0]:
                    continue
                col.remove(i)
                col.add(0)
                moved = True
                continue
            if j in east[i + 1]:
                continue
            if i + 1 not in col:
                col.remove(i)
                col.add(i + 1)
                moved = True
    return moved


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    east = []
    dims = [0, 0]
    lines = list(enumerate(prob_input))
    for i, line in lines:
        dims[0] = max(dims[0], i + 1)
        line_east_cucumbers = SortedSet()
        for j, cucumber in enumerate(line):
            dims[1] = max(dims[1], j + 1)
            if cucumber == '>':
                line_east_cucumbers.add(j)
        east.append(line_east_cucumbers)

    south = [SortedSet() for _ in range(dims[1])]
    for i, line in lines:
        for j, cucumber in enumerate(line):
            if cucumber == 'v':
                south[j].add(i)

    debug("Initial state:")
    draw(east, south, dims)
    dims = tuple(dims)
    moved = True
    step = 1
    while moved:
        moved_east = move_east(east, south, dims)
        moved_south = move_south(east, south, dims)
        moved = moved_east or moved_south
        # draw(east, south, dims)
        step += 1
    return step - 1


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    debug("testing debug")
    return 0


def main():
    run_main(pt_1, pt_2, __file__, [
        58,
        486,
        0,
        0
    ], run_ex=True)


if __name__ == "__main__":
    main()
