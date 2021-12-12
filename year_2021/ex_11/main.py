import logging
from typing import Generator

import numpy as np

from utils.debugging import df
from utils.geometry import Point, Grid
from utils.runner import run_main

logger = logging.getLogger(__name__)


def update_flashed(energies: Grid, flashed: set[Point], p: Point) -> bool:
    any_flash = True
    energies[p] = 0
    flashed.add(p)
    neighbours = energies.get_neighbours(p, diag=True)
    for neigh in neighbours:
        if neigh not in flashed:
            energies[neigh] += 1
    return any_flash


def pt_1(prob_input: Generator) -> int:
    energies = Grid.from_str(prob_input)
    df(energies)
    flashes = 0
    for _ in range(100):
        flashed = set()
        energies += 1
        any_flash = True
        while any_flash:
            any_flash = False
            for p in energies.argwhere(lambda h: h > 9):
                flashes += 1
                any_flash = update_flashed(energies, flashed, p)

    return flashes


def pt_2(prob_input: Generator) -> int:
    energies = Grid.from_str(prob_input)
    df(energies)
    total = np.prod(energies.dims)
    step = 0
    while True:
        step += 1
        energies += 1
        flashed = set()
        any_flash = True
        while any_flash:
            any_flash = False
            for p in energies.argwhere(lambda h: h > 9):
                any_flash = update_flashed(energies, flashed, p)

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
