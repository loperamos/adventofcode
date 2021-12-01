from pathlib import Path
from typing import List

from utils.files import int_list

test_input_1 = [
]
test_input_2 = [
]


def pt_1(prob_input: List):
    return prob_input


def pt_2(prob_input: List):
    return prob_input


if __name__ == "__main__":
    d = Path(__file__).parent
    input_1 = d / "input_1.txt"
    input_2 = d / "input_2.txt"

    # Reader
    reader = int_list
    # Part 1
    print(pt_1(test_input_1))
    print(pt_1(reader(input_1)))

    # Part 2
    print(pt_2(test_input_1))
    print(pt_2(reader(input_1)))
