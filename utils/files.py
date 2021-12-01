from pathlib import Path
from typing import List


def int_list(path: Path) -> List[int]:
    with path.open() as f:
        return [int(line.rstrip()) for line in f.readlines()]
