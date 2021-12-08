import os.path
from pathlib import Path
from typing import Generator


def line_generator(file_name: str = "exercise.txt") -> Generator[str, None, None]:
    path = Path(os.path.curdir) / "inputs" / file_name
    with path.open() as f:
        for line in f.readlines():
            yield line.rstrip()
