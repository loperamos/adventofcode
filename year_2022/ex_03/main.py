import logging
from string import ascii_lowercase, ascii_uppercase
from typing import Generator

from utils.debugging import debug, info
from utils.runner import run_main

logger = logging.getLogger(__name__)


points_lower = {l: i + 1 for i, l in enumerate(ascii_lowercase)}
points_upper = {l: i + 27 for i, l in enumerate(ascii_uppercase)}

points = points_upper | points_lower
debug(f"{points=}")


def pt_1(prob_input: Generator) -> int:
    p = 0
    for line in prob_input:
        rs = list(line)
        debug(rs)
        size = len(rs)
        debug(len(rs))
        left, right = set(rs[0 : int(size / 2)]), set(rs[int(size / 2) :])
        debug(f"{left=}, {right=}")
        for c in left:
            if c in right:
                debug(c)
                p += points[c]

    return p


def pt_2(prob_input: Generator) -> int:
    p = 0
    lines = [set(l) for l in prob_input]
    n_rs = int(len(lines) / 3)
    for i in range(n_rs):
        a = lines[i * 3]
        b = lines[i * 3 + 1]
        c = lines[i * 3 + 2]
        info(f"{a=}, {b=}, {c=}")
        same = a & b & c
        info(f"{same=}")
        p += points[same.pop()]

    return p


def main():
    run_main(pt_1, pt_2, __file__, [157, 7568, 70, 0])


if __name__ == "__main__":
    main()
