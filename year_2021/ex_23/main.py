import logging
import sys
from dataclasses import dataclass
from enum import Enum
from itertools import product
from queue import PriorityQueue
from typing import Generator, Any, Optional

import numpy as np
from numpy.typing import NDArray

from utils.debugging import debug, print_array, array_to_str, df
from utils.runner import run_main

logger = logging.getLogger(__name__)


class AnphType(Enum):
    A = 1
    B = 10
    C = 100
    D = 1000


TYPE_TO_HOLES = {
    AnphType.A: {(2, 3), (3, 3), (4, 3), (5, 3)},
    AnphType.B: {(2, 5), (3, 5), (4, 5), (5, 5)},
    AnphType.C: {(2, 7), (3, 7), (4, 7), (5, 7)},
    AnphType.D: {(2, 9), (3, 9), (4, 9), (5, 9)}
}

HOLE_TO_TYPE = {
    3: AnphType.A,
    5: AnphType.B,
    7: AnphType.C,
    9: AnphType.D,
}


@dataclass(frozen=True)
class State:
    s: NDArray
    t: tuple[str]
    energy: int = 0

    def __lt__(self, other):
        # if self.get_finished() > other.get_finished():
        #     return True
        # if self.get_finished() < other.get_finished():
        #     return False
        return self.energy < other.energy

    def __hash__(self):
        return hash(self.t)

    def __eq__(self, other):
        return self.t == other.t

    def get_finished(self) -> int:
        count = 0
        for anph_type, locs in self.get_element_positions().items():
            for loc in locs:
                if loc in TYPE_TO_HOLES[anph_type] and self.col_is_correct(loc[1]):
                    count += 1
        return count

    @staticmethod
    def t_from_s(s: NDArray) -> tuple[str]:
        return tuple("".join(l) for l in s)

    @classmethod
    def from_lines(cls, lines: list[str]):
        s = np.full([len(lines), 13], ' ')
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                s[i, j] = c
        t = cls.t_from_s(s)
        return State(s, t)

    def print_debug(self):
        debug("---------------------------")
        debug(f"{self.energy=}")
        for l in self.s:
            debug("".join(l))

    def str_debug(self):
        out = f"---------------------------\n" \
              f"{self.energy=}\n"
        for l in self.s:
            out += "".join(l) + '\n'
        return out

    def is_final(self, final) -> bool:
        return self == final

    def can_stop(self, loc_start, loc, anph_type: AnphType) -> bool:
        # can't stop at intersection
        if loc in {(1, 3), (1, 5), (1, 7), (1, 9)}:
            return False

        if loc[0] == 1:
            # Can't stop on the line if coming from the line, otherwise, moving to top line is allowed
            return loc_start[0] != 1

        # cant stop above empty
        bellow = loc[0] + 1, loc[1]
        if self.s[bellow] == '.':
            return False

        # not his hole
        if loc not in TYPE_TO_HOLES[anph_type]:
            return False

        if loc in TYPE_TO_HOLES[anph_type] and not self.col_is_correct(loc[1]):
            return False

        return True

    def col_is_correct(self, col):
        for i in range(2, self.s.shape[0]):
            v = self.s[i, col]
            if v == '.':
                continue
            if v == "#":
                return True
            if v != HOLE_TO_TYPE[col].name:
                return False
        return True

    def can_move(self, from_loc, to_loc, anph_type: AnphType) -> bool:
        c = self.s[to_loc]

        # cannot move to non empty spaces
        if c != '.':
            return False

        # always can move to top row
        if to_loc[0] == 1:
            return True

        # if coming from top row, can't move into hole
        if from_loc[0] < to_loc[0] and to_loc not in TYPE_TO_HOLES[anph_type] and not self.col_is_correct(to_loc[1]):
            return False
        return True

    def is_in_place(self, loc: tuple[int, int], anph_type: AnphType) -> bool:
        type_locs = TYPE_TO_HOLES[anph_type]
        if loc not in type_locs:
            return False
        bellow_loc = loc[0] + 1, loc[1]
        bellow = self.s[bellow_loc]
        while bellow != '#':
            if bellow != anph_type.name:
                return False
            bellow_loc = bellow_loc[0] + 1, bellow_loc[1]
            bellow = self.s[bellow_loc]
        return True

    def get_moves(self, loc: tuple[int, int], anph_type: AnphType) -> set[tuple[int, int]]:
        if self.is_in_place(loc, anph_type):
            return set()
        new_moves: set[tuple[int, int]] = set()
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_loc = loc[0] + i, loc[1] + j
            if self.can_move(loc, new_loc, anph_type):
                new_moves.add(new_loc)

        return new_moves

    def move(self, old_loc, new_loc, anph_type: AnphType, cost) -> 'State':
        new_s = np.copy(self.s)
        new_s[old_loc] = '.'
        new_s[new_loc] = anph_type.name
        t = self.t_from_s(new_s)
        return State(new_s, t, self.energy + cost)

    def find_fast_track(self, loc, anph_type: AnphType) -> Optional['State']:
        checked_locs = set()
        next_moves = list((move, anph_type.value) for move in self.get_moves(loc, anph_type))
        while next_moves:
            next_move, cost = next_moves.pop()
            if next_move in checked_locs:
                continue
            checked_locs.add(next_move)
            if self.is_in_place(next_move, anph_type):
                return self.move(loc, next_move, anph_type, cost)
            next_moves.extend((move, cost + anph_type.value) for move in self.get_moves(next_move, anph_type))
        return None

    def get_possible_states(self, loc, anph_type: AnphType) -> set['State']:
        next_states = set()
        checked_locs = set()
        next_moves = list((move, anph_type.value) for move in self.get_moves(loc, anph_type))
        while next_moves:
            next_move, cost = next_moves.pop()
            if next_move in checked_locs:
                continue
            checked_locs.add(next_move)
            if self.can_stop(loc, next_move, anph_type):
                next_states.add(self.move(loc, next_move, anph_type, cost))
            next_moves.extend((move, cost + anph_type.value) for move in self.get_moves(next_move, anph_type))
        return next_states

    def get_element_positions(self):
        return {
            anph_type: {tuple(p) for p in np.argwhere(self.s == anph_type.name)} for anph_type in AnphType
        }

    def get_next_options(self, init_pos: NDArray) -> set['State']:
        pass

    def __repr__(self) -> str:
        return array_to_str(self.s)

    def __str__(self):
        return self.__repr__()

    def get_next_steps(self) -> [set['State'], bool]:
        next_steps = set()
        fast_track = False
        for anph_type, locs in self.get_element_positions().items():
            for loc in locs:
                fast_track_state = self.find_fast_track(loc, anph_type)
                if fast_track_state is not None:
                    fast_track = True
                    next_steps.add(fast_track_state)
                    break
                next_steps.update(self.get_possible_states(loc, anph_type))
            if fast_track:
                break
        return next_steps, fast_track


FINAL_STATE = State.from_lines([
    "#############",
    "#...........#",
    "###A#B#C#D###",
    "  #A#B#C#D#  ",
    "  #########  ",
])

FINAL_STATE_2 = State.from_lines([
    "#############",
    "#...........#",
    "###A#B#C#D###",
    "  #A#B#C#D#  ",
    "  #A#B#C#D#  ",
    "  #A#B#C#D#  ",
    "  #########  ",
])


@dataclass
class StateChain:
    state: State
    chain: list[State]

    def __lt__(self, other):
        return self.state < other.state


def solve_naive(initial_state: State, final_state: State, print_debug=False) -> StateChain:
    to_check: PriorityQueue[StateChain] = PriorityQueue()
    to_check.put(StateChain(initial_state, [initial_state]))
    checked = set()
    while to_check.not_empty:
        checking_chain = to_check.get()
        if checking_chain.state in checked:
            continue
        checked.add(checking_chain.state)
        if print_debug:
            checking_chain.state.print_debug()
        if checking_chain.state == final_state:
            debug("!!!!FOUND!!!!")
            checking_chain.state.print_debug()
            return checking_chain

        possible_new_states, fast_track = checking_chain.state.get_next_steps()
        for new_state in possible_new_states:
            if new_state not in checked:
                # new_chain = checking_chain.chain + [new_state]
                new_chain = []
                if len(new_chain) > 40:
                    continue
                to_check.put(StateChain(new_state, new_chain))
        if fast_track:
            continue
    raise Exception("We should not be here")


def pt_1(prob_input: Generator[str, Any, None]):
    s = State.from_lines(list(prob_input))
    return solve_naive(s, FINAL_STATE, False).state.energy


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    # return 0
    lines = list(prob_input)
    lines = lines[:3] + [
        "  #D#C#B#A#  ",
        "  #D#B#A#C#  "
    ] + lines[3:]
    s = State.from_lines(lines)
    s.print_debug()
    return solve_naive(s, FINAL_STATE_2, False).state.energy


def main():
    run_main(pt_1, pt_2, __file__, [
        12521,
        15338,
        44169,
        47064
    ], run_ex=True)


if __name__ == "__main__":
    main()
