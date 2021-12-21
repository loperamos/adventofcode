from dataclasses import dataclass
from itertools import product
from typing import Generator, Any, Callable, Iterable

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation

NO_ROTATION = Rotation.from_euler('x', 0, degrees=True)

SINGLE_AXIS_ROTATIONS = [
    NO_ROTATION,
    Rotation.from_euler('x', 90, degrees=True),
    Rotation.from_euler('x', 180, degrees=True),
    Rotation.from_euler('x', 270, degrees=True),
    Rotation.from_euler('yx', [180, 0], degrees=True),
    Rotation.from_euler('yx', [180, 90], degrees=True),
    Rotation.from_euler('yx', [180, 180], degrees=True),
    Rotation.from_euler('yx', [180, 270], degrees=True)
]

NEW_AXIS_ROTATION = Rotation.from_euler('xy', [-90, -90], degrees=True)

ALL_ROTATIONS: list[Rotation] = [a * b for a, b in product([NO_ROTATION, NEW_AXIS_ROTATION, NEW_AXIS_ROTATION * NEW_AXIS_ROTATION], SINGLE_AXIS_ROTATIONS)]


@dataclass
class Point:
    arr: NDArray[int]
    tup: tuple[int, ...]
    dim: int

    def __init__(self, *vals: int, arr: NDArray[int] = None):
        if arr is not None:
            if len(arr.shape) != 1:
                raise Exception("Wrong arr in input, shape must be 1D")
            self.arr = np.rint(arr).astype(int)
            self.tup = tuple(self.arr)
            self.dim = self.arr.shape[0]
            return

        self.arr = np.array(vals)
        self.tup = tuple(vals)
        self.dim = len(vals)

    def rotate(self, rotation: Rotation) -> 'Point':
        rotated_arr = rotation.apply(self.arr)
        return Point(arr=rotated_arr)

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
        return self.tup == other.tup

    def __setitem__(self, key, value):
        if key > self.dim:
            raise Exception(f"Position {key} out of dimensions {self.dim}")
        self.arr[key] = value

    def __getitem__(self, item: int) -> int:
        if item > self.dim:
            raise Exception(f"Position {item} out of dimensions {self.dim}")
        return self.arr[item]

    def __add__(self, other) -> 'Point':
        return Point(arr=self.arr + other.arr)

    def __sub__(self, other) -> 'Point':
        return Point(arr=self.arr - other.arr)

    def __mul__(self, other) -> 'Point':
        return Point(arr=self.arr * other)

    def __repr__(self) -> str:
        return "(" + ", ".join(str(n) for n in self.tup).rstrip(", ") + ")"

    def __str__(self) -> str:
        return self.__repr__()

    def __lt__(self, other):
        for i in range(self.dim):
            if self[i] == other[i]:
                continue
            return self[i] < other[i]
        return False

    def zeros(self):
        return not self.arr.any()


def rotate_points(points: Iterable[Point], rotation: Rotation) -> list[Point]:
    arrays = np.array([p.arr for p in points])
    return [Point(arr=a) for a in rotation.apply(arrays)]


def get_all_points_rotations(points: Iterable[Point]) -> Generator[tuple[list[Point], Rotation], Any, None]:
    arrays = np.array([p.arr for p in points])
    return (([Point(arr=a) for a in r.apply(arrays)], r) for r in ALL_ROTATIONS)


def get_all_rotations(point: Point):
    return [point.rotate(r) for r in ALL_ROTATIONS]


@dataclass(frozen=True)
class Grid:
    dims: NDArray[int]
    vals: NDArray

    @classmethod
    def from_arr(cls, array: NDArray):
        return Grid(np.array(array.shape), array)

    @classmethod
    def from_str(cls, line_generator: Generator[str, Any, None]) -> 'Grid':
        lines = list(line_generator)
        dims = np.array([len(lines), len(lines[0])])
        matrix = np.zeros(dims, dtype=int)
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


def multidim_range(*dims: int) -> Generator[tuple[int, ...], Any, None]:
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
