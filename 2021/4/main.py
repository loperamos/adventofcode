import logging
from collections import defaultdict
from pprint import pformat
from typing import *
import numpy as np

from utils.debugging import d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    board_vals, boards, boards_counting, draws = prepare_data(prob_input)

    for draw in draws:
        d(f"{draw=}")
        for board_id, loc in boards[draw].items():
            i, j = loc
            d(f"{board_id=}, ({i=}, {j=})")
            current_count_v = boards_counting[board_id]["v"][j]
            current_count_h = boards_counting[board_id]["h"][i]
            if len(current_count_v) == 4 or len(current_count_h) == 4:
                d(pformat(board_vals[board_id]))
                return (sum(board_vals[board_id]) - draw) * draw
            boards_counting[board_id]["v"][j].add(draw)
            boards_counting[board_id]["h"][i].add(draw)
            board_vals[board_id].remove(draw)
        # d(pformat(boards_counting))
    return 0


def pt_2(prob_input: Generator) -> int:
    board_vals, boards, boards_counting, draws = prepare_data(prob_input)

    last_winning_board = None

    for draw in draws:
        d(f"{draw=}")
        if len(boards_counting) == 1:
            last_winning_board = next(iter(boards_counting.keys()))
            d(pformat(board_vals[last_winning_board]))
        for board_id, loc in boards[draw].items():
            if board_id not in boards_counting:
                continue
            if last_winning_board is not None and board_id != last_winning_board:
                continue
            i, j = loc
            d(f"{board_id=}, ({i=}, {j=})")
            current_count_v = boards_counting[board_id]["v"][j]
            current_count_h = boards_counting[board_id]["h"][i]
            if len(current_count_v) == 4 or len(current_count_h) == 4:
                if last_winning_board is not None:
                    return (sum(board_vals[board_id]) - draw) * draw
                else:
                    d(pformat(board_vals[board_id]))
                    del boards_counting[board_id]
                    continue

            boards_counting[board_id]["v"][j].add(draw)
            boards_counting[board_id]["h"][i].add(draw)
            board_vals[board_id].remove(draw)
        d(pformat(boards_counting))
    return 0


def prepare_data(prob_input):
    draws = (int(draw) for draw in prob_input.__next__().split(','))
    d(f"{draws=}")
    boards = defaultdict(dict)
    board_vals = []
    board_id = 0
    i = 0
    prob_input.__next__()
    for line in prob_input:
        if line == "":
            i = 0
            board_id += 1
            continue

        if i == 0:
            board_vals.append(set())
        for j, num in enumerate(line.split()):
            board_vals[board_id].add(int(num))
            boards[int(num)][board_id] = (i, j)

        i += 1
    boards_counting = {board: {"v": {j: set() for j in range(5)}, "h": {j: set() for j in range(5)}} for board in range(board_id + 1)}
    return board_vals, boards, boards_counting, draws


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
