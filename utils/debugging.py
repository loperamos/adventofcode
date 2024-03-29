import logging
from pprint import pformat

import coloredlogs
import numpy as np
from numpy.typing import NDArray

FIELD_STYLES = dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', bold=True),
    name=dict(color='blue'),
    programname=dict(color='cyan'),
    username=dict(color='yellow'),
)

coloredlogs.install(level='DEBUG', field_styles=FIELD_STYLES)

logger = logging.getLogger(__name__)
forced_no_debug = False
handler = logging.StreamHandler()
handler.terminator = ""


def force_no_debug():
    global forced_no_debug
    forced_no_debug = True


def set_logger(new_logger) -> None:
    global logger
    logger = new_logger


def set_debug(debug: bool = False) -> None:
    global forced_no_debug
    logger.setLevel(logging.DEBUG if debug and not forced_no_debug else logging.INFO)


def df(item: object) -> None:
    debug("\n" + pformat(item))


def info_format(item: object) -> None:
    info("\n" + pformat(item))


def debug(msg: object) -> None:
    logger.debug(msg)


def info(msg: object) -> None:
    logger.info(msg)


def array_to_str(arr: NDArray) -> str:
    return np.array2string(arr, max_line_width=100000)


def print_array_as_str(arr: NDArray, dbg: bool = True):
    for l in arr:
        if dbg:
            debug("".join(l))
        else:
            info("".join(l))


def print_array(arr: NDArray) -> None:
    debug("\n" + array_to_str(arr))
