import logging
import re
from typing import Generator

from utils.runner import run_main

logger = logging.getLogger(__name__)


action_re = re.compile(r"move (\d+) from (\d) to (\d)")


def parse_queues(prob_input: Generator) -> list[list[str]]:
    queues_info = []
    for line in prob_input:
        if line == "":
            break
        queues_info.append(line)

    queues: list[list[str]] = []
    n_queues = int(queues_info[-1][-2])
    for i_q in range(n_queues):
        pos = 1 + i_q * 4
        queues.append([])
        for q_data in reversed(queues_info[:-1]):
            if pos >= len(q_data):
                break
            q_v = q_data[pos]
            if q_v == " ":
                break
            queues[-1].append(q_v)
    return queues


def pt_1(prob_input: Generator) -> str:
    queues = parse_queues(prob_input)

    for action in prob_input:
        m = action_re.match(action)
        assert m, f"Whats going on? {action=}"
        count, q_from, q_to = int(m[1]), int(m[2]), int(m[3])
        for _ in range(count):
            queues[q_to - 1].append(queues[q_from - 1].pop())

    return "".join([q[-1] for q in queues])


def pt_2(prob_input: Generator) -> str:
    queues = parse_queues(prob_input)

    for action in prob_input:
        m = action_re.match(action)
        assert m, f"Whats going on? {action=}"
        count, q_from, q_to = int(m[1]), int(m[2]), int(m[3])
        tmp = []
        for _ in range(count):

            tmp.append(queues[q_from - 1].pop())
        queues[q_to - 1].extend(reversed(tmp))

    return "".join([q[-1] for q in queues])


def main():
    run_main(pt_1, pt_2, __file__, ["CMZ", "JCMHLVGMG", "MCD", "LVMRWSSPZ"])


if __name__ == "__main__":
    main()
