import logging
from typing import Generator

import numpy as np

from utils.debugging import debug
from utils.runner import run_main

# logger = logging.getLogger(__name__)

action = {
    "forward": np.array([0, 1]),
    "up": np.array([-1, 0]),
    "down": np.array([1, 0]),
}


def read_line(line: str) -> np.array:
    action_str, amount = line.split()
    return action[action_str] * int(amount)


def pt_1(prob_input: Generator) -> int:
    position = sum(read_line(line) for line in prob_input)
    return position[0] * position[1]


def pt_2(prob_input: Generator) -> int:
    position = [0, 0]
    aim = 0
    for line in prob_input:
        a = read_line(line)
        if a[1] != 0:
            position[1] += a[1]
            position[0] += a[1] * aim
        else:
            aim += a[0]
        debug(f"{aim=}, {position=}")

    return position[0] * position[1]


def main():
    run_main(pt_1, pt_2, __file__, [
        150,
        1451208,
        900,
        1620141160
    ])


if __name__ == "__main__":
    main()
