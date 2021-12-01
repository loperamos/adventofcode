import os.path
from pathlib import Path
from typing import List, Generator


def int_list(file_name: str = "input_1.txt") -> List[int]:
    path = Path(os.path.curdir) / file_name
    with path.open() as f:
        return [int(line.rstrip()) for line in f.readlines()]


def line_generator(file_name: str = "input_1.txt") -> Generator[str, None, None]:
    path = Path(os.path.curdir) / file_name
    with path.open() as f:
        for line in f.readlines():
            yield line.rstrip()
