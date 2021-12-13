import logging
from typing import Generator, Any

import numpy as np
from numpy.typing import NDArray

from utils.debugging import d, df, info
from utils.geometry import Point
from utils.runner import run_main

logger = logging.getLogger(__name__)


def fold(matrix: NDArray, axis, line: int):
    n, m = matrix.shape
    if axis == "y":
        for j in range(line + 1, n):
            for i in range(m):
                if matrix[j, i] == 1:
                    fold_j = 2 * line - j
                    matrix[fold_j, i] = 1
        return matrix[:line, :]
    else:
        for i in range(line + 1, m):
            for j in range(n):
                if matrix[j, i] == 1:
                    fold_i = 2 * line - i
                    matrix[j, fold_i] = 1
        return matrix[:, :line]


def parse_input(prob_input):
    dims = np.zeros(2, dtype=int)
    points = set()
    for line in prob_input:
        if line == "":
            break
        i, j = line.split(',')
        points.add(Point(int(i), int(j)))
        dims[0] = max(dims[0], int(i))
        dims[1] = max(dims[1], int(j))
    instructions = []
    for line in prob_input:
        axis, val = line.split()[2].split("=")
        instructions.append((axis, int(val)))

    matrix = np.zeros(dims + 1, dtype=int)
    for p in points:
        matrix[p.i, p.j] = 1
    matrix = matrix.T
    return instructions, matrix


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    instructions, matrix = parse_input(prob_input)
    df(matrix)

    folded = fold(matrix, instructions[0][0], instructions[0][1])
    return folded.sum().sum()


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    instructions, matrix = parse_input(prob_input)

    for ins in instructions:
        matrix = fold(matrix, ins[0], ins[1])

    matrix_str = matrix.astype(str)
    matrix_str[matrix_str == "1"] = "#"
    matrix_str[matrix_str == "0"] = " "
    info("\n" + np.array2string(matrix_str, max_line_width=400))

    return matrix.sum().sum()


def main():
    run_main(pt_1, pt_2, __file__, [
        17,
        827,
        16,
        104
    ])


if __name__ == "__main__":
    main()
