import logging
from typing import *

from utils.debugging import d
from utils.runner import run_main

logger = logging.getLogger(__name__)


def pt_1(prob_input: Generator) -> int:
    d("testing debug")
    return 0


def pt_2(prob_input: Generator) -> int:
    d("testing debug")
    return 0


if __name__ == "__main__":
    run_main(pt_1, pt_2, logger)
