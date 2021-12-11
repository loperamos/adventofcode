import os.path
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Any


def _get(path: Path) -> Generator[str, Any, None]:
    with path.open() as f:
        for line in f.readlines():
            yield line.rstrip()


@dataclass
class LineGen:
    folder: Path

    @property
    def test(self) -> Generator[str, Any, None]:
        return _get(self.folder / "inputs" / "test")

    @property
    def exercise(self) -> Generator[str, Any, None]:
        return _get(self.folder / "inputs" / "exercise")


def line_generator(file_name: str = "exercise.txt") -> Generator[str, None, None]:
    path = Path(os.path.curdir) / "inputs" / file_name
    with path.open() as f:
        for line in f.readlines():
            yield line.rstrip()
