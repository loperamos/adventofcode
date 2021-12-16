import logging
import math
from typing import Generator, Any

from utils.runner import run_main

logger = logging.getLogger(__name__)


def hex_to_bin(hex_str):
    return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)


type_to_op = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda a: 1 if a[0] > a[1] else 0,
    6: lambda a: 1 if a[0] < a[1] else 0,
    7: lambda a: 1 if a[0] == a[1] else 0,
}


def compute_num(bin_num, idx) -> tuple[int, int]:
    n = ""
    while bin_num[idx] != "0":
        idx += 1
        n += bin_num[idx:idx + 4]
        idx += 4
    idx += 1
    n += bin_num[idx:idx + 4]
    idx += 4
    return idx, int(n, 2)


def compute_package(bin_num, idx, max_l) -> tuple[int, int]:
    sum_v = 0
    done = False
    while (max_l is not None and idx < max_l) or (not done):
        done = True
        v = bin_num[idx: idx + 3]
        sum_v += int(v, 2)
        idx += 3
        t = bin_num[idx: idx + 3]
        idx += 3
        if t == "100":
            idx, _ = compute_num(bin_num, idx)
        else:
            l_id = bin_num[idx]
            idx += 1
            if l_id == "0":
                length = int(bin_num[idx: idx + 15], 2)
                idx += 15
                idx, new_sum = compute_package(bin_num, idx, idx + length)
                sum_v += new_sum
            else:
                count = int(bin_num[idx: idx + 11], 2)
                idx += 11
                for _ in range(count):
                    idx, new_sum = compute_package(bin_num, idx, None)
                    sum_v += new_sum
    return idx, sum_v


def pt_1(prob_input: Generator[str, Any, None]) -> list[int]:
    res = []
    for i, line in enumerate(prob_input):
        bin_num = hex_to_bin(line)
        _, sum_v = compute_package(bin_num, 0, None)
        res.append(sum_v)
    return res


def compute_package_2(bin_num, idx) -> tuple[int, int, int]:
    sum_v = 0
    v = bin_num[idx: idx + 3]
    sum_v += int(v, 2)
    idx += 3
    t = bin_num[idx: idx + 3]
    idx += 3
    if t == "100":
        idx, n = compute_num(bin_num, idx)
        return idx, sum_v, n

    l_id = bin_num[idx]
    idx += 1
    nums = []
    if l_id == "0":
        length = int(bin_num[idx: idx + 15], 2)
        idx += 15
        max_ids = idx + length
        while idx < max_ids:
            idx, new_sum, n = compute_package_2(bin_num, idx)
            nums.append(n)
            sum_v += new_sum
    else:
        count = int(bin_num[idx: idx + 11], 2)
        idx += 11
        nums = []
        for _ in range(count):
            idx, new_sum, n = compute_package_2(bin_num, idx)
            sum_v += new_sum
            nums.append(n)
    return idx, sum_v, type_to_op[int(t, 2)](nums)


def pt_2(prob_input: Generator[str, Any, None]) -> list[int]:
    res = []
    for i, line in enumerate(prob_input):
        bin_num = hex_to_bin(line)
        _, _, n = compute_package_2(bin_num, 0)
        res.append(n)
    return res


def main():
    run_main(pt_1, pt_2, __file__, [
        [14, 8, 15, 11, 13, 19, 16, 20, 6, 9, 14, 16, 12, 23, 31],
        [996],
        [3, 54, 7, 9, 1, 0, 0, 1, 2021, 1, 3, 15, 46, 46, 54],
        [96257984154]
    ])


if __name__ == "__main__":
    main()
