import copy
import logging
from dataclasses import dataclass
from itertools import permutations
from math import ceil, floor
from typing import Generator, Any, Optional

from utils.runner import run_main

logger = logging.getLogger(__name__)


def try_parse_int(val_str) -> Optional[int]:
    try:
        return int(val_str)
    except ValueError:
        return None


@dataclass
class Node:
    left: Optional['Node'] = None
    right: Optional['Node'] = None
    value: Optional[int] = None

    def set_val(self, val: int):
        self.left = None
        self.right = None
        self.value = val

    @property
    def is_val(self):
        return self.value is not None

    def __add__(self, other):
        return copy.deepcopy(Node(self, other))

    def __repr__(self):
        if self.value is None:
            return f"[{self.left},{self.right}]"
        else:
            return f"{self.value}"

    def __eq__(self, other):
        if self.value is None:
            return self.left == other.left and self.right == other.right
        else:
            return self.value == other.value

    def magnitude(self) -> int:
        if self.is_val:
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @classmethod
    def from_str(cls, line: str) -> 'Node':

        v = try_parse_int(line)
        if v is not None:
            return Node(value=v)

        line = line[1:-1]

        count = 0
        for i, char in enumerate(line):
            if char == "[":
                count += 1
            elif char == "]":
                count -= 1
            elif count == 0 and char == ",":
                l = line[:i]
                r = line[i + 1:]
                break
        l_val = Node.from_str(l)
        r_val = Node.from_str(r)
        return Node(l_val, r_val)

    def try_split(self) -> bool:
        if self.is_val and self.value >= 10:
            self.left = Node(value=floor(self.value / 2))
            self.right = Node(value=ceil(self.value / 2))
            self.value = None
            return True
        return False


def reduce(node):
    reduced = True
    while reduced:
        reduced = False
        reduced |= explode_all(node) | split(node)


def split(node: Node) -> bool:
    stack = [node]
    while stack:
        check = stack.pop()
        if check.try_split():
            return True
        if check.is_val:
            continue
        stack.append(check.right)
        stack.append(check.left)
    return False


def explode_all(node: Node) -> bool:
    exploded = True
    while exploded:
        exploded = explode(node)
    return exploded


def explode(node: Node) -> bool:
    last_node = None
    stack: list[tuple[Node, int]] = [(node, 0)]
    right_val = 0
    exploding = False
    while stack:
        check, depth = stack.pop()
        if exploding:
            if check.is_val:
                check.value += right_val
                break
            stack.append((check.right, depth + 1))
            stack.append((check.left, depth + 1))
            continue
        if depth == 4:
            if check.is_val:
                last_node = check
                continue
            if last_node is not None:
                last_node.value += check.left.value
            right_val = check.right.value
            check.set_val(0)
            exploding = True
            continue

        if check.is_val:
            last_node = check
            continue

        stack.append((check.right, depth + 1))
        stack.append((check.left, depth + 1))
        continue
    return exploding


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    added_line = Node.from_str(prob_input.__next__())
    for line in prob_input:
        added_line += Node.from_str(line)
        reduce(added_line)
    return added_line.magnitude()


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    options = [Node.from_str(line) for line in prob_input]
    max_val = 0
    for a, b in permutations(options, 2):
        n = a + b
        reduce(n)
        mag = n.magnitude()
        max_val = max(max_val, mag)
    return max_val


def main():
    run_main(pt_1, pt_2, __file__, [
        4140,
        4323,
        3993,
        4749
    ])


if __name__ == "__main__":
    main()
