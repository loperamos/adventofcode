import logging

import coloredlogs

coloredlogs.install(level='DEBUG')

logger = logging.getLogger(__name__)


def set_logger(new_logger) -> None:
    global logger
    logger = new_logger


def set_debug(debug: bool = False) -> None:
    logger.setLevel(logging.DEBUG if debug else logging.INFO)


def d(msg: str) -> None:
    logger.debug(msg)


def i(msg: str) -> None:
    logger.info(msg)
