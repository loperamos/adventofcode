import logging
import re
from typing import Generator

import portion as p  # type: ignore

from utils.runner import run_main

logger = logging.getLogger(__name__)

intervals_re = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")


def get_intervals(line: str) -> tuple[p.Interval, p.Interval]:
    m = intervals_re.match(line)
    assert m, "We should have matches"
    return p.closed(int(m[1]), int(m[2])), p.closed(int(m[3]), int(m[4]))


def pt_1(prob_input: Generator) -> int:
    contained = 0
    for line in prob_input:
        i_a, i_b = get_intervals(line)
        if i_a.contains(i_b) or i_b.contains(i_a):
            contained += 1
    return contained


def pt_2(prob_input: Generator) -> int:
    overlapping = 0
    for line in prob_input:
        i_a, i_b = get_intervals(line)
        if i_a.overlaps(i_b):
            overlapping += 1

    return overlapping


def main():
    run_main(pt_1, pt_2, __file__, [2, 500, 4, 815])


if __name__ == "__main__":
    main()
