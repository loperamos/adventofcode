from dataclasses import dataclass
from itertools import product
from typing import Generator, Any, Callable

import numpy as np
from numpy.typing import NDArray


@dataclass
class Point:
    arr: NDArray[int]
    tup: tuple[int, ...]
    dim: int

    def __init__(self, *vals: int, arr: NDArray[int] = None):
        if arr is not None:
            if len(arr.shape) != 1:
                raise Exception("Wrong arr in input, shape must be 1D")
            self.arr = arr.copy()
            self.tup = tuple(arr)
            self.dim = arr.shape[0]
            return

        self.arr = np.array(vals)
        self.tup = tuple(vals)
        self.dim = len(vals)

    @property
    def i(self) -> int:
        return self.arr[0]

    @property
    def j(self) -> int | None:
        if self.dim < 2:
            return None
        return self.arr[1]

    @property
    def k(self) -> int | None:
        if self.dim < 3:
            return None
        return self.arr[2]

    def __hash__(self) -> int:
        return hash(self.tup)

    def __eq__(self, other) -> bool:
        return self.i == other.i and self.j == other.j

    def __getitem__(self, item: int) -> int:
        if item > self.dim:
            raise Exception(f"Position {item} out of dimensions {self.dim}")
        return self.arr[item]

    def __add__(self, other) -> 'Point':
        return Point(arr=self.arr + other.arr)

    def __mul__(self, other) -> 'Point':
        return Point(arr=self.arr * other)

    def __repr__(self) -> str:
        return "(" + ", ".join(str(n) for n in self.tup).rstrip(", ") + ")"

    def __str__(self) -> str:
        return self.__repr__()

    def zeros(self):
        return not self.arr.any()


@dataclass(frozen=True)
class Grid:
    dims: NDArray[int]
    vals: NDArray

    @classmethod
    def from_str(cls, line_generator: Generator[str, Any, None]) -> 'Grid':
        lines = list(line_generator)
        dims = np.array([len(lines), len(lines[0])])
        matrix = np.zeros(dims)
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                matrix[i, j] = int(c)
        return Grid(dims, matrix)

    def items(self) -> Generator[tuple[Point, int], Any, None]:
        for c in multidim_range(*self.dims):
            p = Point(*c)
            yield p, self[p]

    def points(self) -> Generator[Point, Any, None]:
        for c in multidim_range(*self.dims):
            yield Point(*c)

    def argwhere(self, condition: Callable[[int], bool]) -> Generator[Point, Any, None]:
        return (p for p, v in self.items() if condition(v))

    def __getitem__(self, point: Any) -> int:
        if isinstance(point, Point):
            return self._get_from_point(point)
        elif isinstance(point, tuple):
            return self._get_from_tuple(point)
        raise AttributeError("Invalid input type")

    def __setitem__(self, point: Any, val: int):
        if isinstance(point, Point):
            self.vals.itemset(point.tup, val)
        elif isinstance(point, tuple):
            self.vals.itemset(point, val)
        else:
            raise AttributeError("Invalid input type")

    def _get_from_point(self, point: Point) -> int:
        if point.dim != len(self.dims):
            raise Exception(f"Point {point} has the wrong number of dimensions. Expected {len(self.dims)}")
        return self._get_from_tuple(point.tup)

    def _get_from_tuple(self, tup: tuple[int, ...]) -> int:
        if len(tup) != len(self.dims):
            raise Exception(f"Tup {tup} has the wrong number of dimensions. Expected {len(self.dims)}")
        k = self.vals
        for c in tup:
            k = k[c]
        return int(k)

    def __contains__(self, point: Point) -> bool:
        for i, v in enumerate(point.tup):
            if v < 0 or v >= self.dims[i]:
                return False
        return True

    def get_neighbours(self, point: Point, diag: bool) -> Generator[Point, Any, None]:
        neighbours_gen = diag_neighbours if diag else straight_neighbours
        return (point + n for n in neighbours_gen(len(self.dims)) if point + n in self and point + n != point)

    def __add__(self, other: int) -> 'Grid':
        return Grid(self.dims, self.vals + other)

    def __mul__(self, other: int) -> 'Grid':
        return Grid(self.dims, self.vals * other)

    def __eq__(self, other):
        return np.array_equal(self.dims, other.dims) and np.array_equal(self.vals, other.vals)

    def __repr__(self) -> str:
        return f"Grid(dims={self.dims.tolist()}, vals={self.vals.tolist()})"

    def __str__(self) -> str:
        return self.__repr__()


def multidim_range(*dims: int) -> Generator[tuple[int], Any, None]:
    ranges = (range(dim) for dim in dims)
    return (p for p in product(*ranges))


def straight_neighbours(n_dims) -> Generator[Point, Any, None]:
    arr = np.zeros(n_dims, dtype=int)
    for i in range(n_dims):
        a = arr.copy()
        a[i] = 1
        yield Point(arr=a)
        yield Point(arr=-a)


def diag_neighbours(n_dims) -> Generator[Point, Any, None]:
    for coords in product(*(range(-1, 2) for _ in range(n_dims))):
        p = Point(*coords)
        if p.zeros():
            continue
        yield p
