import logging
from typing import Generator, Any

from utils.debugging import debug
from utils.runner import run_main
from year_2021.ex_22.cube import Cube

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    grid_on = set()
    for line in prob_input:
        cube = Cube.from_line(line)
        if not cube.bounded():
            continue
        for p in cube.points():
            if cube.on:
                grid_on.add(p)
            elif p in grid_on:
                grid_on.remove(p)
    return len(grid_on)


def merge_cubes(cubes_to_check: list[Cube]) -> set['Cube']:
    active_independent_cubes: set[Cube] = {cubes_to_check[0]}

    for cube in cubes_to_check[1:]:
        if cube.on:
            cubes_to_add_check = [cube]
            cubes_to_add = set()
            while cubes_to_add_check:
                to_check = cubes_to_add_check.pop()
                valid = True
                for final_cube in active_independent_cubes:
                    if to_check.inside_of(final_cube):
                        valid = False
                        break
                    if to_check.collides(final_cube):
                        cubes_to_add_check.extend(to_check.split_by(final_cube))
                        valid = False
                        break
                if valid:
                    cubes_to_add.add(to_check)
            active_independent_cubes.update(cubes_to_add)
        else:
            to_remove = set()
            to_add = set()
            for final_cube in active_independent_cubes:
                if not cube.collides(final_cube):
                    continue
                to_remove.add(final_cube)
                for piece in final_cube.split_by(cube):
                    if not piece.inside_of(cube):
                        to_add.add(piece)
            active_independent_cubes.difference_update(to_remove)
            active_independent_cubes.update(to_add)
    return active_independent_cubes


def compute_on(cubes_to_check: list[Cube]):
    merged = merge_cubes(cubes_to_check)
    return sum(cube.size() for cube in merged)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    input_cubes = [Cube.from_line(line) for line in prob_input]
    debug(f"{input_cubes=}")
    return compute_on(input_cubes)


def main():
    run_main(pt_1, pt_2, __file__, [
        474140,
        503864,
        2758514936282235,
        1255547543528356
    ], run_ex=True)


if __name__ == "__main__":
    main()
