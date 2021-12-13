import logging
from pathlib import Path
from typing import List, Callable, Generator

from utils.debugging import info, set_debug, set_logger
from utils.files import LineGen


def run_main(pt_1: Callable[[Generator], int], pt_2: Callable[[Generator], int], file: str, results: List[int]):
    folder = Path(file).parent
    logger = logging.getLogger(folder.name)
    set_logger(logger)

    line_gen = LineGen(folder)

    info("\n\n")
    info("********************************************" + '*' * len(folder.name))
    info(f"*                     {folder.name}                     *")
    info("********************************************" + '*' * len(folder.name))

    info("  --------------------------------------------")
    info("  |                  part 1                  |")
    info("  --------------------------------------------")
    set_debug(True)
    p1_test = pt_1(line_gen.test)
    set_debug(False)
    p1_exer = pt_1(line_gen.exercise)

    info("  --------------------------------------------")
    info("  |                  part 2                  |")
    info("  --------------------------------------------")
    set_debug(True)
    p2_test = pt_2(line_gen.test)
    set_debug(False)
    p2_exer = pt_2(line_gen.exercise)

    info(f"\tPart 1 test: {p1_test}")
    info(f"\tPart 1 result: {p1_exer}")
    info(f"\tPart 2 test: {p2_test}")
    info(f"\tPart 2 result: {p2_exer}")

    assert p1_test == results[0], f"{p1_test=} != {results[0]=}"
    assert p1_exer == results[1], f"{p1_exer=} != {results[1]=}"
    assert p2_test == results[2], f"{p2_test=} != {results[2]=}"
    assert p2_exer == results[3], f"{p2_exer=} != {results[3]=}"
