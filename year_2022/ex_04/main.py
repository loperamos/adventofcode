import logging
from typing import Generator

from utils.debugging import debug
from utils.runner import run_main

logger = logging.getLogger(__name__)


def is_inside(section_a, section_b) -> bool:
    return section_a[0] >= section_b[0] and section_a[1] <= section_b[1]


def pt_1(prob_input: Generator) -> int:
    p = 0
    for line in prob_input:
        elf_a, elf_b = line.split(",")
        sa = elf_a.split("-")
        sb = elf_b.split("-")
        sa = int(sa[0]), int(sa[1])
        sb = int(sb[0]), int(sb[1])
        debug(f"{sa=}, {sb=}")
        if is_inside(sa, sb):
            debug(f"overlaps a in b")
            p += 1
        elif is_inside(sb, sa):
            debug(f"overlaps b in a")
            p += 1

    return p


def overlaps(section_a, section_b) -> bool:
    # ..3...7
    # ...4..7

    return section_a[0] <= section_b[0] <= section_a[1] or section_a[0] <= section_b[1] <= section_a[1]


def pt_2(prob_input: Generator) -> int:
    p = 0
    for line in prob_input:
        elf_a, elf_b = line.split(",")
        sa = elf_a.split("-")
        sb = elf_b.split("-")

        sa = int(sa[0]), int(sa[1])
        sb = int(sb[0]), int(sb[1])
        debug(f"{sa=}, {sb=}")
        if overlaps(sa, sb):
            debug(f"overlaps a in b")
            p += 1
        elif overlaps(sb, sa):
            debug(f"overlaps b in a")
            p += 1

    return p


def main():
    run_main(pt_1, pt_2, __file__, [2, 500, 4, 0])


if __name__ == "__main__":
    main()
