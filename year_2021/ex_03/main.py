import logging
from typing import Generator

import numpy as np

from utils.debugging import df, d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    lines = list(prob_input)
    summing = np.zeros(len(lines[0]))
    for line in lines:
        for i, bit in enumerate(line):
            summing[i] += int(bit) * 2 - 1

    d(f"{summing=}")
    o_b = ""
    c_b = ""
    for b in summing:
        if b > 0:
            o_b += "1"
            c_b += "0"
        else:
            o_b += "0"
            c_b += "1"
    return int(o_b, 2) * int(c_b, 2)


def pt_2(prob_input: Generator) -> int:
    bits = [list(line) for line in prob_input]
    df(bits)
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


def main():
    run_main(pt_1, pt_2, __file__, [
        198,
        3912944,
        230,
        4996233
    ])


if __name__ == "__main__":
    main()
