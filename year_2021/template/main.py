import logging
from typing import Generator, Any

from utils.debugging import d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator[str, Any, None]) -> int:
    d("testing debug")
    return 0


def pt_2(prob_input: Generator[str, Any, None]) -> int:
    d("testing debug")
    return 0


def main():
    run_main(pt_1, pt_2, __file__, [
        0,
        0,
        0,
        0
    ])


if __name__ == "__main__":
    main()
