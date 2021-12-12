import logging
from dataclasses import dataclass
from pprint import pformat
from typing import Generator, Any

from utils.debugging import d, df
from utils.runner import run_main

logger = logging.getLogger(__name__)


@dataclass
class Node:
    id: str
    big: bool
    connected: set[str]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


END = Node("end", False, set())
START = Node("start", False, set())


def build_nodes(prob_input: Generator[str, Any, None]) -> dict[str, Node]:
    nodes: dict[str, Node] = {}
    for line in prob_input:
        left, right = line.split('-')
        if left not in nodes:
            nodes[left] = Node(left, left.isupper(), set())
        if right not in nodes:
            nodes[right] = Node(right, right.isupper(), set())

        nodes[left].connected.add(right)
        nodes[right].connected.add(left)
    return nodes


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    nodes = build_nodes(prob_input)

    start = nodes['start']
    stack: list[tuple[Node, set[Node], str]] = [(start, {start}, "start")]

    paths: set[str] = set()
    while stack:
        node, path, str_path = stack.pop()
        if node == END:
            paths.add(str_path)
            continue

        for next_node_id in node.connected:
            next_node = nodes[next_node_id]
            if not next_node.big and next_node in path:
                continue
            new_path = path.union({next_node})
            stack.append((next_node, new_path, str_path + f"-{next_node.id}"))
    d(f"\n{pformat(sorted(paths))}")
    return len(paths)


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    nodes = build_nodes(prob_input)

    start = nodes['start']
    stack: list[tuple[Node, set[Node], bool, str]] = [(start, {start}, False, "start")]

    paths: set[str] = set()
    while stack:
        node, path, twice, str_path = stack.pop()
        if node == END:
            paths.add(str_path)
            continue

        for next_node_id in node.connected:
            next_node = nodes[next_node_id]
            new_twice = twice
            if next_node == START:
                continue
            if not next_node.big and next_node in path:
                if twice:
                    continue
                else:
                    new_twice = True
            new_path = path.union({next_node})
            stack.append((next_node, new_path, new_twice, str_path + f"-{next_node.id}"))
    d(f"\n{pformat(sorted(paths))}")
    return len(paths)


def main():
    run_main(pt_1, pt_2, __file__, [
        10,
        5874,
        36,
        153592
    ])


if __name__ == "__main__":
    main()
