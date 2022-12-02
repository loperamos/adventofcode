from enum import Enum
from typing import Generator

from utils.debugging import debug
from utils.runner import run_main


class Choice(Enum):
    ROCK: str = "A"
    PAPER: str = "B"
    SCISSORS: str = "C"


same = {"X": "A", "Y": "B", "Z": "C"}

points = {Choice.ROCK: 1, Choice.PAPER: 2, Choice.SCISSORS: 3}

choices = list(Choice)

beats = {c: choices[i - 1] for i, c in enumerate(choices)}
loses = {l: b for b, l in beats.items()}


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
        elf_raw, me_raw = line.split()
        elf = Choice(elf_raw)
        me = Choice(same[me_raw])
        total += get_points(me, elf)
        debug(f"{me=}, {elf=} -> {total=}")

    return total


def pt_2(prob_input: Generator) -> int:
    total = 0

    for line in prob_input:
        elf_raw, me_result = line.split()
        elf = Choice(elf_raw)
        if me_result == "X":
            me = beats[elf]
        elif me_result == "Y":
            me = elf
        else:
            me = loses[elf]
        total += get_points(me, elf)
    return total


def main():
    run_main(pt_1, pt_2, __file__, [15, 15337, 12, 11696])


if __name__ == "__main__":
    main()
