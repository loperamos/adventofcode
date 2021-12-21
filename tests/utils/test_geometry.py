from itertools import product
from scipy.spatial.transform import Rotation

import numpy as np

from utils.geometry import Point, Grid, multidim_range, diag_neighbours, straight_neighbours, rotate_points, NEW_AXIS_ROTATION, get_all_points_rotations, get_all_rotations


def test_new_axis():
    points = [Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1)]
    print(rotate_points(points, NEW_AXIS_ROTATION * NEW_AXIS_ROTATION * NEW_AXIS_ROTATION))


def test_rotate_points():
    points = [Point(1, 2, 3), Point(4, 3, 2)]
    all_rots = get_all_points_rotations(points)
    print(list(all_rots))


def test_compare():
    a = Point(1, 2)
    b = Point(2, 1)
    assert b < a


def test_print_point():
    p = Point(1, 2, 3)
    print(p)
    p_r = p.rotate(Rotation.from_euler('x', 90, degrees=True))
    print(p_r)


def test_point_operations():
    p_1 = Point(0, 1, 5, 6, 3)
    assert p_1 + p_1 == p_1 * 2


def test_point_operations_arr():
    p_1 = Point(arr=np.array([0, 1, 5, 6, 3]))
    assert p_1 + p_1 == p_1 * 2


def test_multidim_range():
    normal_ranges = (p for p in product(range(2), range(3), range(4)))
    multidim_ranges = multidim_range(2, 3, 4)
    for left, right in zip(normal_ranges, multidim_ranges):
        assert left == right


def test_grid():
    lines = [
        "1234",
        "3455",
        "8765"
    ]

    grid = Grid.from_str(line for line in lines)
    assert grid[Point(2, 1)] == 7
    assert grid[2, 1] == 7


def test_diag_neighbours():
    assert set(diag_neighbours(2)) == {Point(-1, -1), Point(-1, 0), Point(-1, 1), Point(0, -1), Point(0, 1), Point(1, -1), Point(1, 0), Point(1, 1)}


def test_straight_neighbours():
    assert set(straight_neighbours(2)) == {Point(-1, 0), Point(0, -1), Point(0, 1), Point(1, 0)}


def test_neighbours():
    lines = [
        "1234",
        "3455",
        "8765"
    ]

    grid = Grid.from_str(line for line in lines)
    straight_n = set(grid.get_neighbours(Point(1, 0), diag=False))
    diag_n = set(grid.get_neighbours(Point(1, 0), diag=True))
    assert straight_n == {Point(0, 0), Point(1, 1), Point(2, 0)}
    assert diag_n == {Point(0, 0), Point(1, 1), Point(2, 0), Point(0, 1), Point(2, 1)}


def test_grid_sum():
    lines = [
        "12",
        "13"
    ]

    grid = Grid.from_str(line for line in lines)

    lines_add = [
        "23",
        "24"
    ]
    grid_add = Grid.from_str(line for line in lines_add)
    assert (grid + 1) == grid_add


def test_grid_iterate():
    lines = [
        "12",
        "13"
    ]

    grid = Grid.from_str(line for line in lines)
    assert set(grid.items()) == {(Point(0, 0), 1), (Point(1, 0), 1), (Point(0, 1), 2), (Point(1, 1), 3)}
