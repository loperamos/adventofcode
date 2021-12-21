import logging
import re
from dataclasses import dataclass
from itertools import permutations
from queue import PriorityQueue
from typing import Generator, Any

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation

from utils.geometry import Point, get_all_points_rotations, rotate_points, NO_ROTATION
from utils.runner import run_main
from year_2021.ex_19.scanner_array import ScannerArray

logger = logging.getLogger(__name__)

re_scanner = re.compile(r'--- scanner (\d+) ---')


@dataclass
class Scanner:
    beacons: list[Point]
    id: int

    def __init__(self, id: int, beacons: list[Point] = None):
        self.id = id
        self.beacons = beacons if beacons is not None else []

    def add_beacon(self, line: str):
        self.beacons.append(Point(*[int(c) for c in line.split(',')]))

    def rotations(self) -> Generator[tuple['Scanner', Rotation], Any, None]:
        return ((Scanner(self.id, points), r) for points, r in get_all_points_rotations(self.beacons))

    def get_shifted_beacons(self, p: Point) -> dict[Point, int]:
        return {b - p: i for i, b in enumerate(self.beacons)}

    def rotate(self, r: Rotation):
        return Scanner(self.id, rotate_points(self.beacons, r))

    def transform(self, r: Rotation, disp: Point):
        return Scanner(self.id, [p + disp for p in rotate_points(self.beacons, r)])

    def get_with_ids(self, ids: set[int]) -> list[Point]:
        return [self.beacons[i] for i in ids]

    def __repr__(self):
        ret = f"--- scanner {self.id} ---\n"
        for b in self.beacons:
            ret += f"{b}\n"
        return ret

    @classmethod
    def from_generator(cls, input_gen: Generator):
        id_line = input_gen.__next__()
        s_id_match = re_scanner.match(id_line)
        scanner = Scanner(int(s_id_match.group(1)))
        for line in input_gen:
            if line == "":
                break
            scanner.add_beacon(line)
        return scanner


def int_rot(r: Rotation):
    return np.rint(r.as_matrix()).astype(int)


def get_scanners(prob_input):
    scanners: dict[int, ScannerArray] = {}
    finished = False
    while not finished:
        try:
            scanner = ScannerArray.from_generator(prob_input)
            scanners[scanner.id] = scanner
        except StopIteration:
            finished = True
    return scanners


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    scanners = get_scanners(prob_input)
    transforms_to_0: dict[int, tuple[Rotation, NDArray[int]]] = {
        0: (NO_ROTATION, np.array([0, 0, 0]))
    }
    absolute_points = set(scanners[0].tuples)

    match_found = False

    q = PriorityQueue()
    q.put(0)

    to_check = set(scanners.keys()) - {0}
    while not q.empty():
        sa_id = q.get()
        for sb_id in to_check.copy():
            sa = scanners[sa_id]
            for sb_rotated, Rba in scanners[sb_id].rotations():
                for beacon_a in sa.beacons:
                    shifted_a = set(sa.translated(-beacon_a).tuples)
                    for beacon_b in sb_rotated.beacons:
                        shifted_b = set(sb_rotated.translated(-beacon_b).tuples)
                        overlap = shifted_a & shifted_b
                        if len(overlap) >= 12:
                            dba = beacon_a - beacon_b
                            r_a0, da0 = transforms_to_0[sa_id]
                            db0 = r_a0.apply(dba) + da0
                            r_b0 = r_a0 * Rba
                            transforms_to_0[sb_id] = (r_b0, db0)

                            sb_transformed = scanners[sb_id].transform(r_b0, db0)
                            absolute_points |= set(sb_transformed.tuples)
                            match_found = True
                            q.put(sb_id)
                            to_check.remove(sb_id)

                            break
                    if match_found:
                        break
                if match_found:
                    match_found = False
                    break
    return len(absolute_points)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    scanners = get_scanners(prob_input)
    transforms_to_0: dict[int, tuple[Rotation, NDArray[int]]] = {
        0: (NO_ROTATION, np.array([0, 0, 0]))
    }

    match_found = False

    q = PriorityQueue()
    q.put(0)

    to_check = set(scanners.keys()) - {0}
    while not q.empty():
        sa_id = q.get()
        for sb_id in to_check.copy():
            sa = scanners[sa_id]
            for sb_rotated, Rba in scanners[sb_id].rotations():
                for beacon_a in sa.beacons:
                    shifted_a = set(sa.translated(-beacon_a).tuples)
                    for beacon_b in sb_rotated.beacons:
                        shifted_b = set(sb_rotated.translated(-beacon_b).tuples)
                        overlap = shifted_a & shifted_b
                        if len(overlap) >= 12:
                            dba = beacon_a - beacon_b
                            r_a0, da0 = transforms_to_0[sa_id]
                            db0 = r_a0.apply(dba) + da0
                            r_b0 = r_a0 * Rba
                            transforms_to_0[sb_id] = (r_b0, db0)
                            match_found = True
                            q.put(sb_id)
                            to_check.remove(sb_id)

                            break
                    if match_found:
                        break
                if match_found:
                    match_found = False
                    break

    max_dist = 0
    for a, b in permutations(transforms_to_0.items(), 2):
        a_id, tr_a = a
        b_id, tr_b = b

        _, disp_a = tr_a
        _, disp_b = tr_b
        dist = round(sum(np.abs(disp_b - disp_a)))
        max_dist = max(max_dist, dist)
    return max_dist


def main():
    run_main(pt_1, pt_2, __file__, [
        79,
        318,
        3621,
        12166
    ], run_ex=True)


if __name__ == "__main__":
    main()
