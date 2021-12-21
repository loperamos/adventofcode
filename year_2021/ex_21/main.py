import logging
from collections import Counter
from itertools import product
from typing import Generator, Any

import numpy as np

from utils.debugging import debug, print_array
from utils.runner import run_main

logger = logging.getLogger(__name__)


def roll_100(r):
    if r < 98:
        return r + 3, r * 3 + 3
    if r == 98:
        return 1, r * 3 + 3
    if r == 99:
        return 2, 200
    if r == 100:
        return 3, 103


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    points = [
        int(prob_input.__next__()[-1]),
        int(prob_input.__next__()[-1])
    ]
    s = [0, 0]

    nr = 1
    rolls = 0

    next_p = 0
    while s[0] < 1000 and s[1] < 1000:
        nr, r = roll_100(nr)
        rolls += 3
        landed = (points[next_p] + r - 1) % 10 + 1
        s[next_p] += landed
        points[next_p] = landed
        next_p = (next_p + 1) % 2

    debug(f"{rolls=}, {s=}")
    if s[0] >= 1000:
        return rolls * s[1]
    return rolls * s[0]


def get_new_pos(positions, r):
    return (positions[0] % r) + 1, (positions[1] % r) + 1


def get_new_score(s, p):
    return s[0] + p[0], s[1] + p[1]


def roll_iterative(p):
    check = [(p, (0, 0), r) for r in range(2, 9)]

    victories = np.array([0, 0])

    while check:
        p, s, r = check.pop()
        debug(f"pos: {p}, score: {s}, roll: {r}, {victories=}, {len(check)=}")
        p = get_new_pos(p, r)
        s = get_new_score(s, p)

        if s[0] >= 21:
            victories += np.array([1, 0])
        elif s[1] >= 21:
            victories += np.array([0, 1])
        else:
            for r in range(2, 9):
                check.append((p, s, r))


def get_universes_per_roll(roll_options, roll_count):
    return Counter(sum(c) for c in product(roll_options, repeat=roll_count))


def solve_dp(init_pos, max_score=21, max_pos=10, roll_options=None, roll_count=3):
    def get_next_step(p, s, roll):
        next_p = (p + roll - 1) % max_pos + 1
        ns = s + next_p
        ns = min(ns, max_score)
        return next_p, ns

    roll_options = roll_options if roll_options else [1, 2, 3]
    universes_per_roll = get_universes_per_roll(roll_options, roll_count)

    dp = np.zeros([max_pos + 1, max_pos + 1, max_score + 1, max_score + 1, 2, 2], dtype='int64')
    dp[:, :, :, max_score, 0, 1] = 1
    dp[:, :, max_score, :, 1, 0] = 1
    for sa in reversed(range(max_score)):
        for sb in reversed(range(max_score)):
            for pa in range(1, max_pos + 1):
                for pb in range(1, max_pos + 1):
                    for player in range(2):
                        for r, u in universes_per_roll.items():
                            if player == 0:
                                next_pos, next_score = get_next_step(pa, sa, r)
                                dp[pa, pb, sa, sb, 0] += dp[next_pos, pb, next_score, sb, 1] * u
                            if player == 1:
                                next_pos, next_score = get_next_step(pb, sb, r)
                                dp[pa, pb, sa, sb, 1] += dp[pa, next_pos, sa, next_score, 0] * u

    print_array(dp[init_pos[0], init_pos[1], 0, 0, 0])
    return dp[init_pos[0], init_pos[1], 0, 0, 0][0]


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    positions = [
        int(prob_input.__next__()[-1]),
        int(prob_input.__next__()[-1])
    ]

    init_a = positions[0]
    init_b = positions[1]
    max_score = 21
    max_pos = 10
    rolls = [1, 2, 3]
    roll_count = 3

    dp = solve_dp((init_a, init_b), max_score, max_pos, rolls, roll_count)
    return dp


def main():
    run_main(pt_1, pt_2, __file__, [
        739785,
        797160,
        444356092776315,
        27464148626406
    ], run_ex=True)


if __name__ == "__main__":
    # print(sys.maxsize)
    main()
