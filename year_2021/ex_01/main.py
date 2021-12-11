import logging
from typing import Generator

from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    as_list = list(prob_input)
    ret = 0
    prev = as_list[0]
    for i in as_list:
        if i > prev:
            ret += 1
        prev = i
    return ret


def pt_2(prob_input: Generator) -> int:
    as_list = list(prob_input)
    ret = 0
    i = 1
    j = 3
    while j < len(as_list):
        if as_list[j] > as_list[i - 1]:
            ret += 1
        i += 1
        j += 1
    return ret


def main():
    run_main(pt_1, pt_2, __file__, [
        7,
        1789,
        5,
        1816
    ])


if __name__ == "__main__":
    main()
