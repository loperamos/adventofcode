import logging
from enum import Enum
from typing import Generator

from utils.debugging import d, df
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    counting = 0
    for line in prob_input:
        test, output = line.split(" | ")
        d(f"{test=}, {output=}")
        for attempt in output.split():
            if len(attempt) in {2, 3, 4, 7}:
                counting += 1

    return counting


class Segment(Enum):
    TOP = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    MID = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6


num_to_segments = {
    0: {Segment.TOP, Segment.TOP_RIGHT, Segment.TOP_LEFT, Segment.BOTTOM_LEFT, Segment.BOTTOM_RIGHT, Segment.BOTTOM},
    1: {Segment.TOP_RIGHT, Segment.BOTTOM_RIGHT},
    2: {Segment.TOP, Segment.TOP_RIGHT, Segment.MID, Segment.BOTTOM_LEFT, Segment.BOTTOM},
    3: {Segment.TOP, Segment.TOP_RIGHT, Segment.MID, Segment.BOTTOM_RIGHT, Segment.BOTTOM},
    4: {Segment.TOP_LEFT, Segment.TOP_RIGHT, Segment.MID, Segment.BOTTOM_RIGHT},
    5: {Segment.TOP, Segment.TOP_LEFT, Segment.MID, Segment.BOTTOM_RIGHT, Segment.BOTTOM},
    6: {Segment.TOP, Segment.TOP_LEFT, Segment.MID, Segment.BOTTOM_RIGHT, Segment.BOTTOM_RIGHT, Segment.BOTTOM},
    7: {Segment.TOP, Segment.TOP_RIGHT, Segment.BOTTOM_RIGHT},
    8: set(Segment),
    9: {Segment.TOP, Segment.TOP_RIGHT, Segment.TOP_LEFT, Segment.MID, Segment.BOTTOM_RIGHT, Segment.BOTTOM},
}

len_to_num = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}


def pt_2(prob_input: Generator) -> int:
    counting = 0
    for line in prob_input:
        wires_to_number = {}
        segment_to_wires = {v: set(c for c in "abcdefg") for v in Segment}
        tests, outputs = line.split(" | ")
        for test_vals in sorted(tests.split(), key=len):
            wires = set(test_vals)
            length = len(wires)
            # Easy case
            if length in len_to_num:
                n = len_to_num[length]
                wires_to_number["".join(sorted(wires))] = n
                num_segments = num_to_segments[n]
                for segment in Segment:
                    if segment not in num_segments:
                        segment_to_wires[segment] -= wires
                for segment in num_segments:
                    segment_to_wires[segment] &= wires
            elif length == 5:
                if len(wires & segment_to_wires[Segment.TOP_RIGHT] & segment_to_wires[Segment.BOTTOM_RIGHT]) == 2:
                    wires_to_number["".join(sorted(wires))] = 3
                elif len(wires & segment_to_wires[Segment.TOP_LEFT] & segment_to_wires[Segment.MID]) == 2:
                    wires_to_number["".join(sorted(wires))] = 5
                else:
                    wires_to_number["".join(sorted(wires))] = 2
            elif length == 6:
                if len(wires & segment_to_wires[Segment.BOTTOM_LEFT] & segment_to_wires[Segment.BOTTOM]) == 1:
                    wires_to_number["".join(sorted(wires))] = 9
                elif len(wires & segment_to_wires[Segment.TOP_RIGHT] & segment_to_wires[Segment.BOTTOM_RIGHT]) == 2:
                    wires_to_number["".join(sorted(wires))] = 0
                else:
                    wires_to_number["".join(sorted(wires))] = 6

        df(wires_to_number)
        for i, output in enumerate(reversed(outputs.split())):
            counting += wires_to_number["".join(sorted(output))] * 10 ** i

    return counting


def main():
    run_main(pt_1, pt_2, __file__, [
        26,
        479,
        61229,
        1041746
    ])


if __name__ == "__main__":
    main()
