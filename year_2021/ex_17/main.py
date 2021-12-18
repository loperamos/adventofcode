import logging
import re
from collections import defaultdict
from typing import Generator, Any

from utils.debugging import debug, info
from utils.geometry import Point
from utils.runner import run_main

logger = logging.getLogger(__name__)


def drift(p: Point) -> Point:
    arr = p.arr
    if arr[0] > 0:
        arr[0] -= 1
    elif arr[0] < 0:
        arr[0] += 1
    arr[1] -= 1
    return Point(arr=arr)


def try_y(y: int, y_range: tuple[int, int]) -> set[int]:
    debug(f"trying {y=}")
    pos = Point(0, 0)
    velocity = Point(0, y)
    steps = set()
    step = 0
    while pos.j >= y_range[0]:
        debug(f"{pos=}, {velocity=}")
        if pos.j <= y_range[1]:
            steps.add(step)
        pos += velocity
        step += 1
        velocity = drift(velocity)
    return steps


def try_vel(v: Point, x_range, y_range) -> bool:
    debug(f"Trying {v=}")
    pos = Point(0, 0)
    while pos.i <= x_range[1] and pos.j >= y_range[0]:
        if pos.i >= x_range[0] and pos.j <= y_range[1]:
            return True
        pos += v
        v = drift(v)
    return False


def find_y(y_range: tuple[int, int]) -> dict[int, set[int]]:
    step_to_y = defaultdict(set)
    y = 9
    while y <= abs(y_range[0]):
        steps = try_y(y, y_range)
        for step in steps:
            step_to_y[step].add(y)
        y += 1

    return step_to_y


def get_max_y(y):
    return int(y * (y + 1) / 2)


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    x_range, y_range = get_ranges(prob_input)

    info(f"{x_range=}, {y_range=}")

    option_y = find_y(y_range)
    info(f"{option_y=}")

    max_y = 0
    for ies in option_y.values():
        for y in ies:
            max_y = max(max_y, get_max_y(y))

    return max_y


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    x_range, y_range = get_ranges(prob_input)

    count = 0

    for x in range(x_range[1] + 1):
        for y in range(y_range[0], -y_range[0]):
            if try_vel(Point(x, y), x_range, y_range):
                count += 1
    return count


def get_ranges(prob_input):
    re_x = re.compile(r'^target area: x=(\d+)\.\.(\d+), y=(.*)\.\.(.*)$')
    matches = re_x.match(prob_input.__next__())
    x_range = (int(matches.group(1)), int(matches.group(2)))
    y_range = (int(matches.group(3)), int(matches.group(4)))
    info(f"{x_range=}, {y_range=}")
    return x_range, y_range


def main():
    run_main(pt_1, pt_2, __file__, [
        45,
        6786,
        112,
        2313
    ])


if __name__ == "__main__":
    main()
