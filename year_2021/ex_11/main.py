import itertools
import logging
from typing import Generator

import numpy as np

from utils.debugging import df
from utils.runner import run_main

logger = logging.getLogger(__name__)


def update_flashed(energies: np.array, flashed: set, i: int, j: int) -> bool:
    n, m = energies.shape

    def valid(a, b):
        if a < 0 or a >= n:
            return False
        if b < 0 or b >= m:
            return False
        return True

    def get_adjacent():
        for x, y in itertools.product(range(-1, 2), range(-1, 2)):
            if x == 0 and y == 0:
                continue
            if valid(i + x, j + y):
                yield i + x, j + y

    any_flash = True
    energies[i, j] = 0
    flashed.add((i, j))
    neighbours = get_adjacent()
    for neigh in neighbours:
        if neigh not in flashed:
            energies[neigh[0], neigh[1]] += 1
    return any_flash


def pt_1(prob_input: Generator) -> int:
    energies = np.array([[int(p) for p in line] for line in prob_input])
    df(energies)
    flashes = 0
    for _ in range(100):
        flashed = set()
        energies += 1
        any_flash = True
        while any_flash:
            any_flash = False
            for i, j in np.argwhere(energies > 9):
                flashes += 1
                any_flash = update_flashed(energies, flashed, i, j)

    return flashes


def pt_2(prob_input: Generator) -> int:
    energies = np.array([[int(p) for p in line] for line in prob_input])
    df(energies)
    n, m = energies.shape
    total = n * m
    step = 0
    while True:
        step += 1
        energies += 1
        flashed = set()
        any_flash = True
        while any_flash:
            any_flash = False
            for i, j in np.argwhere(energies > 9):
                any_flash = update_flashed(energies, flashed, i, j)

        if len(flashed) == total:
            return step


def main():
    run_main(pt_1, pt_2, __file__, [
        1656,
        1732,
        195,
        290
    ])


if __name__ == "__main__":
    main()
