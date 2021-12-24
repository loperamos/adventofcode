import re
from dataclasses import dataclass
from itertools import product


def range_in_bounds(x_range, y_range, z_range, bounds=50):
    if x_range[0] > bounds or x_range[1] <= -bounds:
        return False
    if y_range[0] > bounds or y_range[1] <= -bounds:
        return False
    if z_range[0] > bounds or z_range[1] <= -bounds:
        return False
    return True


def ranges_collide(range_a: tuple[int, int], range_b: tuple[int, int]) -> bool:
    if range_a[0] == range_b[0] or range_a[1] == range_b[1]:
        return True
    if range_a[0] < range_b[0] < range_a[1]:
        return True
    if range_a[0] < range_b[1] < range_a[1]:
        return True
    if range_b[0] < range_a[0] < range_b[1]:
        return True
    if range_b[0] < range_a[1] < range_b[1]:
        return True
    return False


@dataclass(frozen=True)
class Cube:
    on: bool
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    z_range: tuple[int, int]

    re_line = re.compile(r'^(\w+) x=([\d-]+)\.\.([\d-]+),y=([\d-]+)\.\.([\d-]+),z=([\d-]*)\.\.([\d-]*)$')

    @classmethod
    def from_line(cls, line: str) -> 'Cube':
        match = cls.re_line.match(line)
        on_off = match.group(1)
        x = int(match.group(2)), int(match.group(3)) + 1
        y = int(match.group(4)), int(match.group(5)) + 1
        z = int(match.group(6)), int(match.group(7)) + 1
        return Cube(on_off == 'on', x, y, z)

    def points(self):
        return product(
            range(self.x_range[0], self.x_range[1]),
            range(self.y_range[0], self.y_range[1]),
            range(self.z_range[0], self.z_range[1]))

    def bounded(self, bounds=50):
        if self.x_range[0] > bounds or self.x_range[1] <= -bounds:
            return False
        if self.y_range[0] > bounds or self.y_range[1] <= -bounds:
            return False
        if self.z_range[0] > bounds or self.z_range[1] <= -bounds:
            return False
        return True

    def collides(self, other: 'Cube'):
        if not ranges_collide(self.x_range, other.x_range):
            return False
        if not ranges_collide(self.y_range, other.y_range):
            return False
        if not ranges_collide(self.z_range, other.z_range):
            return False
        return True

    def inside_of(self, other: 'Cube') -> bool:
        if self.x_range[0] < other.x_range[0] or self.x_range[1] > other.x_range[1]:
            return False
        if self.y_range[0] < other.y_range[0] or self.y_range[1] > other.y_range[1]:
            return False
        if self.z_range[0] < other.z_range[0] or self.z_range[1] > other.z_range[1]:
            return False
        return True

    def size(self) -> int:
        return (self.x_range[1] - self.x_range[0]) * (self.y_range[1] - self.y_range[0]) * (self.z_range[1] - self.z_range[0])

    def split_by(self, other: 'Cube') -> set['Cube']:
        at_x = []
        at_y = []
        at_z = []
        for i in [0, 1]:
            if self.x_range[0] < other.x_range[i] < self.x_range[1]:
                at_x.append(other.x_range[i])
        for i in [0, 1]:
            if self.y_range[0] < other.y_range[i] < self.y_range[1]:
                at_y.append(other.y_range[i])
        for i in [0, 1]:
            if self.z_range[0] < other.z_range[i] < self.z_range[1]:
                at_z.append(other.z_range[i])
        return self.split(at_x, at_y, at_z)

    def split(self, at_x: list[int], at_y: list[int], at_z: list[int]) -> set['Cube']:

        it_x = [self.x_range[0]] + at_x + [self.x_range[1]]
        it_y = [self.y_range[0]] + at_y + [self.y_range[1]]
        it_z = [self.z_range[0]] + at_z + [self.z_range[1]]

        new_cubes = set()
        for i in range(len(it_x) - 1):
            for j in range(len(it_y) - 1):
                for k in range(len(it_z) - 1):
                    new_cubes.add(Cube(self.on, (it_x[i], it_x[i + 1]), (it_y[j], it_y[j + 1]), (it_z[k], it_z[k + 1])))
        return new_cubes
