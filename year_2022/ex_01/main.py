import logging
from queue import PriorityQueue
from typing import Generator

from sortedcontainers import SortedList

from utils.debugging import debug, info, df, info_format
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    elves: list[int] = [0]
    last_elve_cals = 0
    most_cals: int = 0
    for cals in prob_input:
        if str(cals) == '':
            most_cals = max(last_elve_cals, most_cals)
            last_elve_cals = 0
        else:
            last_elve_cals += int(cals)
    ret = most_cals
    return ret


def update_top(last_elve_cals: int, top_3: SortedList[int]) -> None:
    if len(top_3) < 3:
        top_3.add(-last_elve_cals)
    elif last_elve_cals > -top_3[-1]:
        top_3.pop()
        top_3.add(-last_elve_cals)
    debug(top_3)


def pt_2(prob_input: Generator) -> int:
    top_3: SortedList[int] = SortedList()
    last_elve_cals = 0
    for cals in prob_input:
        if str(cals) == '':
            update_top(last_elve_cals, top_3)
            last_elve_cals = 0
        else:
            last_elve_cals += int(cals)

    update_top(last_elve_cals, top_3)
    return -sum(top_3)


def main():
    run_main(pt_1, pt_2, __file__, [
        24000, 69310, 45000, 206104
    ])


if __name__ == "__main__":
    main()
