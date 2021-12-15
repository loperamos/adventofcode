import logging
from collections import defaultdict, Counter
from typing import Generator, Any

from utils.debugging import df
from utils.runner import run_main

logger = logging.getLogger(__name__)


def run_problem(prob_input, count):
    polymer = prob_input.__next__()
    prob_input.__next__()
    polymer_pairs = defaultdict(int)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i + 2]
        polymer_pairs[pair] += 1

    insertions = {}
    for line in prob_input:
        a, b = line.split(' -> ')
        insertions[a] = b

    for _ in range(count):
        new_pairs = defaultdict(int)
        for source, val in insertions.items():
            if source not in polymer_pairs:
                continue
            count = polymer_pairs[source]
            new_pairs[source[0] + val] += count
            new_pairs[val + source[1]] += count
            del polymer_pairs[source]
        polymer_pairs |= new_pairs

    df(polymer_pairs)

    count = defaultdict(int)
    for pair, val in polymer_pairs.items():
        count[pair[0]] += val
    count[polymer[-1]] += 1

    vals = count.values()
    return max(vals) - min(vals)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    return run_problem(prob_input, 40)


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    return run_problem(prob_input, 10)


def main():
    run_main(pt_1, pt_2, __file__, [
        1588,
        2768,
        2188189693529,
        2914365137499
    ])


if __name__ == "__main__":
    main()
