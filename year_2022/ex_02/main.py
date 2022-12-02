from enum import Enum
from typing import Generator

from utils.debugging import debug, info
from utils.runner import run_main


class Choice(Enum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'


same = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

points = {
    Choice.ROCK: 1,
    Choice.PAPER: 2,
    Choice.SCISSORS: 3
}
beats = {
    Choice.ROCK: Choice.SCISSORS,
    Choice.PAPER: Choice.ROCK,
    Choice.SCISSORS: Choice.PAPER
}
loses = {
    Choice.ROCK: Choice.PAPER,
    Choice.PAPER: Choice.SCISSORS,
    Choice.SCISSORS: Choice.ROCK
}


def get_points(me: Choice, other: Choice) -> int:
    p = points[me]
    if me == other:
        return p + 3
    if beats[me] == other:
        return p + 6
    return p


def pt_1(prob_input: Generator) -> int:
    total = 0

    for line in prob_input:
        elven_raw, me_raw = line.split()
        elven = Choice(elven_raw)
        me = Choice(same[me_raw])
        total += get_points(me, elven)
        debug(f"{me=}, {elven=} -> {total=}")

    return total


def pt_2(prob_input: Generator) -> int:
    total = 0

    for line in prob_input:
        elven_raw, me_result = line.split()
        elven = Choice(elven_raw)
        if me_result == 'X':
            me = beats[elven]
        elif me_result == 'Y':
            me = elven
        else:
            me = loses[elven]
        total += get_points(me, elven)
    return total


def main():
    run_main(pt_1, pt_2, __file__, [
        15,
        15337,
        12,
        11696
    ])


if __name__ == "__main__":
    main()
