from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class Point:
    arr: NDArray[int]
    tup: tuple[int, ...]
    dim: int

    @classmethod
    def from_array(cls, arr: NDArray[int]) -> 'Point':
        if len(arr.shape) != 1:
            raise Exception("Wrong arr in input, shape must be 1D")
        return Point(arr, tuple(i for i in arr), arr.shape[0])

    @classmethod
    def from_vals(cls, *vals: int) -> 'Point':
        return Point(np.array(vals), tuple(vals), len(vals))

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
        return Point.from_array(self.arr + other.arr)

    def __mul__(self, other: int) -> 'Point':
        return Point.from_array(self.arr * other)

    def __repr__(self) -> str:
        return "(" + ", ".join(str(n) for n in self.tup).rstrip(", ") + ")"

    def __str__(self) -> str:
        return self.__repr__()
