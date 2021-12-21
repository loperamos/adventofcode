import re
from dataclasses import dataclass
from typing import Any, Generator

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation

from utils.geometry import ALL_ROTATIONS

re_scanner = re.compile(r'--- scanner (\d+) ---')


def beacon_from_line(line: str) -> NDArray[int]:
    return np.array([int(c) for c in line.split(',')])


def to_int(a: NDArray) -> NDArray:
    return np.rint(a).astype(int)


def int_rot(r: Rotation):
    return np.rint(r.as_matrix()).astype(int)


@dataclass
class ScannerArray:
    id: int
    beacons: NDArray[int]

    def add_beacon(self, line: str):
        beacon = np.array([int(c) for c in line.split(',')])
        self.beacons = np.append(self.beacons, beacon, axis=1)

    @property
    def tuples(self):
        return map(tuple, self.beacons)

    def rotations(self) -> list[tuple['ScannerArray', Rotation]]:
        ret = []
        for r in ALL_ROTATIONS:
            rotated_beacons = to_int(r.apply(self.beacons))
            ret.append((ScannerArray(self.id, rotated_beacons), r))
        return ret

    def get_shifted_beacons(self, translation: NDArray[int]) -> NDArray[int]:
        return self.beacons - translation

    def translated(self, translation: NDArray[int]):
        return ScannerArray(self.id, to_int(self.beacons + translation))

    def rotate(self, rotation: Rotation):
        return ScannerArray(self.id, to_int(rotation.apply(self.beacons)))

    def transform(self, rotation: Rotation, translation: NDArray[int]):
        return ScannerArray(self.id, to_int(rotation.apply(self.beacons) + translation))

    def get_with_ids(self, ids: list[int]) -> NDArray[int]:
        return np.take(self.beacons, ids)

    def __repr__(self):
        ret = f"--- scannerArray {self.id} ---\n"
        for b in self.beacons:
            ret += f"{b}\n"
        return ret

    @classmethod
    def from_generator(cls, input_gen: Generator):
        id_line = input_gen.__next__()
        s_id_match = re_scanner.match(id_line)
        if not s_id_match:
            raise ValueError(f"Wrong line input: {id_line}")
        beacons = []
        for line in input_gen:
            if line == "":
                break
            beacons.append(beacon_from_line(line))

        scanner = ScannerArray(int(s_id_match.group(1)), np.array(beacons))
        return scanner
