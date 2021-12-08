import os
from pathlib import Path

from utils.debugging import i, set_debug, set_logger
from utils.files import line_generator


def run_main(pt_1, pt_2, logger):
    set_logger(logger)
    i(f"Running day {Path(os.path.curdir).absolute().name}")

    i("--------------------------------------------")
    i("|                  part 1                  |")
    i("--------------------------------------------")
    set_debug(True)
    p1_test = pt_1(line_generator('test'))
    set_debug(False)
    p1_exer = pt_1(line_generator('exercise'))

    i("--------------------------------------------")
    i("|                  part 2                  |")
    i("--------------------------------------------")
    set_debug(True)
    p2_test = pt_2(line_generator('test'))
    set_debug(False)
    p2_exer = pt_2(line_generator('exercise'))

    i(f"\tPart 1 test: {p1_test}")
    i(f"\tPart 1 result: {p1_exer}")
    i(f"\tPart 2 test: {p2_test}")
    i(f"\tPart 2 result: {p2_exer}")
