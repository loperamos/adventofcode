import logging
from string import ascii_lowercase, ascii_uppercase
from typing import Generator

from more_itertools import grouper

from utils.runner import run_main

logger = logging.getLogger(__name__)

points = {l: i + 1 for i, l in enumerate(ascii_lowercase)} | {l: i + 27 for i, l in enumerate(ascii_uppercase)}


def pt_1(prob_input: Generator) -> int:
    p = 0
    for line in prob_input:
        rs_size = len(line) // 2
        same = set(line[0:rs_size]) & set(line[rs_size:])
        p += points[same.pop()]
    return p


def pt_2(prob_input: Generator) -> int:
    p = 0
    for a, b, c in grouper(prob_input, 3):
        same = set(a) & set(b) & set(c)
        p += points[same.pop()]
    return p


def main():
    run_main(pt_1, pt_2, __file__, [157, 7568, 70, 2780])


if __name__ == "__main__":
    main()
