import logging
from collections import defaultdict
from typing import Generator, Any

from utils.debugging import df, debug
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    draws = get_draws(prob_input)
    board_vals, boards, n_boards = get_boards(prob_input)
    boards_counting = init_boards_counting(n_boards)

    for draw in draws:
        debug(f"{draw=}")
        for board_id, loc in boards[draw].items():
            i, j = loc
            debug(f"{board_id=}, ({i=}, {j=})")
            current_count_v = boards_counting[board_id]["v"][j]
            current_count_h = boards_counting[board_id]["h"][i]
            if len(current_count_v) == 4 or len(current_count_h) == 4:
                df(board_vals[board_id])
                return (sum(board_vals[board_id]) - draw) * draw
            boards_counting[board_id]["v"][j].add(draw)
            boards_counting[board_id]["h"][i].add(draw)
            board_vals[board_id].remove(draw)
    return 0


def pt_2(prob_input: Generator) -> int:
    draws = get_draws(prob_input)
    board_vals, boards, n_boards = get_boards(prob_input)
    boards_counting = init_boards_counting(n_boards)

    last_winning_board = None

    for draw in draws:
        debug(f"{draw=}")
        if len(boards_counting) == 1:
            last_winning_board = next(iter(boards_counting.keys()))
            df(board_vals[last_winning_board])
        for board_id, loc in boards[draw].items():
            if board_id not in boards_counting:
                continue
            if last_winning_board is not None and board_id != last_winning_board:
                continue
            i, j = loc
            debug(f"{board_id=}, ({i=}, {j=})")
            current_count_v = boards_counting[board_id]["v"][j]
            current_count_h = boards_counting[board_id]["h"][i]
            if len(current_count_v) == 4 or len(current_count_h) == 4:
                if last_winning_board is not None:
                    return (sum(board_vals[board_id]) - draw) * draw
                df(board_vals[board_id])
                del boards_counting[board_id]
                continue

            boards_counting[board_id]["v"][j].add(draw)
            boards_counting[board_id]["h"][i].add(draw)
            board_vals[board_id].remove(draw)
        df(boards_counting)
    return 0


def get_draws(prob_input: Generator) -> Generator[int, Any, None]:
    return (int(draw) for draw in prob_input.__next__().split(','))


Position = tuple[int, int]
DrawValue = int
BoardId = int


def get_boards(prob_input: Generator) -> tuple[list[set[DrawValue]], dict[DrawValue, dict[BoardId, Position]], int]:
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
    return board_vals, boards, board_id + 1


BoardCounting = dict[BoardId, dict[str, dict[int, set[DrawValue]]]]


def init_boards_counting(n_boards) -> BoardCounting:
    boards_counting = {
        board: {
            "v": {i: set() for i in range(5)},
            "h": {j: set() for j in range(5)}
        } for board in range(n_boards)
    }
    return boards_counting


def main():
    run_main(pt_1, pt_2, __file__, [
        4512,
        45031,
        1924,
        2568
    ])


if __name__ == "__main__":
    main()
