import logging
from dataclasses import dataclass
from math import floor
from typing import Generator, Any

from utils.debugging import debug, df
from utils.runner import run_main

logger = logging.getLogger(__name__)


@dataclass(repr=True)
class Instruction:
    div: int
    add_x: int
    add_y: int

    def apply(self, w, z):
        if z % 26 + self.add_x == w:
            return round(z / self.div)
        return floor(z / self.div) * 26 + self.add_y + w

    def get_zero_w(self, z):
        return z % 26 + self.add_x, floor(z / self.div)


def aggregate_instructions(lines: Generator):
    instructions = []
    for i in range(14):
        for _ in range(4):
            lines.__next__()
        div = int(lines.__next__()[6:])
        add_x = int(lines.__next__()[6:])
        for _ in range(9):
            lines.__next__()
        add_y = int(lines.__next__()[6:])
        lines.__next__()
        lines.__next__()
        instructions.append(Instruction(div, add_x, add_y))
    return instructions


def evaluate(instructions, num):
    num_list = list(map(int, list(str(num))))
    z = 0
    for w, ins in zip(num_list, instructions):
        old_z = z
        z = ins.apply(w, z)
        debug(f"{ins}({w}, {old_z})= {z}")


def find_valid(instructions, valid_nums: list[int]):
    to_check: list[tuple[list[int], int, int]] = [([], 0, 0)]
    while to_check:
        prev, z, idx = to_check.pop()
        if idx > 13:
            num = ''.join(map(str, prev))
            if z == 0:
                return int(num)
            continue
        ins = instructions[idx]
        if ins.add_x <= 0:
            w, min_z = ins.get_zero_w(z)
            if 0 < w < 10:
                to_check.append((prev + [w], min_z, idx + 1))
            else:
                continue
        else:
            for i in valid_nums:
                to_check.append((prev + [i], ins.apply(i, z), idx + 1))


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    instructions = aggregate_instructions(prob_input)
    df(instructions)
    return find_valid(instructions, list(range(1, 10)))


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    instructions = aggregate_instructions(prob_input)
    df(instructions)
    return find_valid(instructions, list(reversed(range(1, 10))))


def main():
    run_main(pt_1, pt_2, __file__, [
        36969794979199,
        36969794979199,
        11419161313147,
        11419161313147
    ])


if __name__ == "__main__":
    main()
