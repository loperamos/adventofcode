import logging
from pprint import pformat
from typing import *

from utils.debugging import d
from utils.files import *
import numpy as np
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Union[List, Generator]) -> int:
    # summing = np.zeros(5)
    # for line in prob_input:
    #     for i, bit in enumerate(line):
    #

    # d(f"{summing=}")
    return 0


def pt_2(prob_input: Union[List, Generator]) -> int:
    bits = [[c for c in line] for line in prob_input]
    d(pformat(bits))
    ox_filter = ""
    co2_filter = ""

    for j in range(len(bits[0])):
        ox_counts = [0, 0]
        co2_counts = [0, 0]
        for i in range(len(bits)):
            num = bits[i][j]
            num_str = ''.join(bits[i][:j + 1])
            if num_str.startswith(ox_filter):
                ox_counts[int(num)] += 1
            if num_str.startswith(co2_filter):
                co2_counts[int(num)] += 1

        if sum(ox_counts) != 1:
            ox_filter += "0" if ox_counts[0] > ox_counts[1] else "1"
        if sum(co2_counts) != 1:
            co2_filter += "0" if co2_counts[0] <= co2_counts[1] else "1"
        else:
            co2_filter += "0" if co2_counts[0] > co2_counts[1] else "1"
    x = int(ox_filter, 2)
    y = int(co2_filter, 2)
    d(f"{x=}, {y=}")
    return x * y


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
