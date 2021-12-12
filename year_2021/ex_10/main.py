import logging
from statistics import median
from typing import Generator

from utils.runner import run_main

logger = logging.getLogger(__name__)

open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}
close_to_open = {v: k for k, v in open_to_close.items()}


def pt_1(prob_input: Generator) -> int:
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    tot = 0
    for line in prob_input:
        stack = []
        for c in line:
            if c in open_to_close:
                stack.append(c)
            else:
                inverted = close_to_open[c]
                if inverted != stack[-1]:
                    tot += points[c]
                    break
                stack.pop()
    return tot


def pt_2(prob_input: Generator) -> int:
    points = {")": 1, "]": 2, "}": 3, ">": 4}

    scores = []
    for line in prob_input:
        stack = []
        error = False
        for c in line:
            if c in open_to_close:
                stack.append(c)
            else:
                inverted = close_to_open[c]
                if inverted != stack[-1]:
                    error = True
                    break
                stack.pop()
        if error:
            continue

        closing_missing = (open_to_close[c] for c in reversed(stack))
        tot = 0
        for c in closing_missing:
            tot *= 5
            tot += points[c]
        scores.append(tot)
    return median(scores)


def main():
    run_main(pt_1, pt_2, __file__, [
        26397,
        462693,
        288957,
        3094671161
    ])


if __name__ == "__main__":
    main()
