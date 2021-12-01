from typing import List

from utils.files import int_list

test_input_1 = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


def pt_1(prob_input: List):
    ret = 0
    prev = prob_input[0]
    for i in prob_input:
        if i > prev:
            ret += 1
        prev = i
    return ret


def pt_2(prob_input: List):
    ret = 0
    i = 1
    j = 3
    while j < len(prob_input):
        if prob_input[j] > prob_input[i - 1]:
            ret += 1
        i += 1
        j += 1
    return ret


if __name__ == "__main__":
    # Reader
    reader = int_list

    # Part 1
    print(pt_1(test_input_1))
    print(pt_1(reader()))

    # Part 2
    print(pt_2(test_input_1))
    print(pt_2(reader()))
