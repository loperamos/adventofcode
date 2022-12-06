import logging
from collections import defaultdict
from queue import Queue
from typing import Generator, Any, TypeVar

from utils.runner import run_main

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class FifoQuickLookup(Queue[_T]):
    counts_dict: dict[_T, int]

    def __init__(self, maxsize=0):
        super().__init__(maxsize)
        self.counts_dict = defaultdict(lambda: 0)

    def put(self, item: _T, block: bool = True, timeout: float | None = None) -> None:
        super(FifoQuickLookup, self).put(item, block, timeout)
        self.counts_dict[item] += 1

    def get(self, block: bool = True, timeout: float | None = None) -> _T:
        item = super(FifoQuickLookup, self).get(block, timeout)
        if self.counts_dict[item] == 1:
            del self.counts_dict[item]
        else:
            self.counts_dict[item] -= 1
        return item

    def shift(self, v) -> bool:
        self.put(v)
        self.get()

        for count in self.counts_dict.values():
            if count > 1:
                return False
        return True


def get_code(s: str, length=4) -> int:
    f = FifoQuickLookup()

    for _, v in zip(range(length), s):
        f.put(v)

    for i in range(length, len(s)):
        v = s[i]
        unique = f.shift(v)
        if unique:
            return i + 1
    return 0


def pt_1(prob_input: Generator[str, Any, None]) -> list[int]:
    ret = [get_code(s, 4) for s in prob_input]
    return ret


def pt_2(prob_input: Generator[str, Any, None]) -> list[int]:
    ret = [get_code(s, 14) for s in prob_input]
    return ret


def main():
    run_main(pt_1, pt_2, __file__, [[7, 5, 6, 10, 11], [1965], [19, 23, 23, 29, 26], [2773]])


if __name__ == "__main__":
    main()
