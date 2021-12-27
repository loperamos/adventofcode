import logging
from copy import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from queue import Queue
from typing import Generator, Any, Optional

import numpy as np
from numpy.typing import NDArray

from utils.debugging import debug, set_logger, print_array_as_str, array_to_str
from utils.files import LineGen
from utils.geometry import Point

logger = logging.getLogger(__name__)


def generate_default_matrix():
    board = np.full((12, 20), " ")
    board[0, :] = list("╔══════════════════╗")
    board[-1, :] = list("╚══════════════════╝")
    board[1:-1, 0] = "║"
    board[1:-1, -1] = "║"

    return board


EMPTY_BOARD = generate_default_matrix()


class PieceType(Enum):
    yellow = 1
    orange = 2
    black = 4


class Piece:
    places_tuple: tuple[Point, ...]
    places: set[Point]
    piece_type: PieceType
    horizontal: bool = False
    top_left: Point

    def __init__(self, places: set[Point]):
        self.places = places
        self.places_tuple = tuple(places)
        self.piece_type = PieceType(len(places))
        if self.piece_type == PieceType.orange:
            self.horizontal = self.places_tuple[0][0] == self.places_tuple[1][0]
        self.top_left = min(self.places)

    def __hash__(self):
        return hash(self.places_tuple)

    def __eq__(self, other):
        return self.places_tuple == other.places_tuple

    def to_array_str(self):
        if self.piece_type == PieceType.yellow:
            return np.array([
                list("┌──┐"),
                list("└──┘")
            ])
        elif self.piece_type == PieceType.orange:
            if self.horizontal:
                return np.array([
                    list("┌──────┐"),
                    list("└──────┘"),
                ])
            return np.array([
                list("┌──┐"),
                list("│  │"),
                list("│  │"),
                list("└──┘")
            ])
        else:
            return np.array([
                list("┌──────┐"),
                list("│      │"),
                list("│      │"),
                list("└──────┘")
            ])


@dataclass
class State:
    pieces: list[Piece]
    pieces_tuple: tuple[Piece, ...]
    holes: set[Point]
    holes_tuple: tuple[Point, ...]
    board: NDArray[int]
    big_piece: int

    def __init__(self, pieces: set[Piece], holes: set[Point]):
        self.pieces = list(pieces)
        self.pieces_tuple = tuple(pieces)
        self.holes = holes
        self.holes_tuple = tuple(holes)
        self.board = np.full((5, 4), -1)
        for i, piece in enumerate(self.pieces):
            if piece.piece_type == PieceType.black:
                self.big_piece = i
            for place in piece.places:
                self.board[place.tup] = i

    def __repr__(self):
        return array_to_str(self.board)

    def __hash__(self):
        return hash(self.pieces_tuple)

    def __eq__(self, other):
        return self.pieces_tuple == other.pieces_tuple

    def is_final(self):
        return self.pieces[self.big_piece].top_left == Point(3, 1)

    def try_move(self, place: Point, hole: Point) -> Optional['State']:
        piece_id = self.board[place.tup]
        piece = self.pieces[piece_id]
        direction = hole - place
        if hole not in self.holes:
            return None
        new_places = set(p + direction for p in piece.places)
        if not new_places.issubset(piece.places | self.holes):
            return None

        new_holes: set[Point] = piece.places - new_places
        if len(new_holes) == 1:
            new_holes.update(self.holes - {hole})
        new_pieces = copy(self.pieces)
        new_pieces[piece_id] = Piece(new_places)
        return State(set(new_pieces), new_holes)

    def get_adjacent(self, hole: Point) -> Generator[Point, Any, None]:
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            to_check = hole + Point(i, j)
            if 0 <= to_check.i <= 4 and 0 <= to_check.j <= 3 and to_check not in self.holes:
                yield to_check

    def compute_next_states(self) -> set['State']:
        new_states = set()
        for hole in self.holes:
            for adj in self.get_adjacent(hole):
                moved = self.try_move(adj, hole)
                if moved is not None:
                    new_states.add(moved)
        return new_states

    @classmethod
    def from_lines(cls, lines: list[str]) -> 'State':
        pieces_places: list[set[Point]] = [set() for _ in range(10)]
        holes: set[Point] = set()

        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                try:
                    id_ = int(c)
                    pieces_places[id_].add(Point(i, j))
                except ValueError:
                    holes.add(Point(i, j))

        pieces = {Piece(places) for places in pieces_places}

        return State(pieces, holes)

    def debug_board(self):
        board = generate_default_matrix()
        for piece in self.pieces:
            top_left = np.array(min(piece.places).arr) * np.array([2, 4]) + np.array([1, 2])
            indices, values = zip(*np.ndenumerate(piece.to_array_str()))
            board[tuple(zip(*list(top_left + indices)))] = values
        print_array_as_str(board)


def solve(initial_state: State, final_state: Optional[State] = None) -> list[State]:
    to_check: Queue[list[State]] = Queue()
    to_check.put([initial_state])
    checked: set[State] = set()

    while to_check:
        path = to_check.get()
        last = path[-1]
        if last in checked:
            continue
        checked.add(last)
        if last.is_final():
            return path
        for new_state in last.compute_next_states():
            to_check.put(path + [new_state])


def run_problem(prob_input: Generator[str, Any, None]) -> None:
    initial_state = State.from_lines(list(prob_input))
    debug(f"Starting solver from initial state:")
    initial_state.debug_board()
    solved_path = solve(initial_state)
    debug(f"Solved in {len(solved_path)} moves")
    for state in solved_path:
        state.debug_board()


def main():
    folder = Path(__file__).parent
    set_logger(logging.getLogger(folder.name))
    line_gen = LineGen(folder)
    run_problem(line_gen.test)


if __name__ == "__main__":
    main()
