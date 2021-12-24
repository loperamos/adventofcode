from utils.debugging import debug, df
from year_2021.ex_22.main import Cube, merge_cubes


def test_cube_stuff():
    c_a = Cube(True, (1, 2), (1, 2), (1, 2))
    c_b = Cube(True, (0, 3), (0, 3), (0, 3))
    assert c_a.inside_of(c_b)
    assert c_a.inside_of(c_a)
    assert c_a.collides(c_b)
    df(c_b.split([1, 2], [1, 2], [1, 2]))


def test_points():
    c_a = Cube(True, (1, 3), (1, 3), (1, 3))
    assert list(c_a.points()) == [(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2), (2, 1, 1), (2, 1, 2), (2, 2, 1), (2, 2, 2)]
    assert len(list(c_a.points())) == c_a.size()


def test_big_case():
    a = Cube.from_line("on x=10..12,y=10..12,z=10..12")
    b = Cube.from_line("on x=11..13,y=11..13,z=11..13")
    c = Cube.from_line("off x=9..11,y=9..11,z=9..11")
    d = Cube.from_line("on x=10..10,y=10..10,z=10..10")
    merged = merge_cubes([a, b, c, d])
    debug(merge_cubes([a, b, c, d]))
    debug(sum(c.size() for c in merged))


def test_merge():
    c_a = Cube(True, (0, 3), (0, 3), (0, 3))
    c_b = Cube(True, (2, 4), (0, 4), (0, 3))
    assert merge_cubes([c_a, c_b]) == {
        Cube(on=True, x_range=(0, 3), y_range=(0, 3), z_range=(0, 3)),
        Cube(on=True, x_range=(3, 4), y_range=(3, 4), z_range=(0, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(3, 4), z_range=(0, 3)),
        Cube(on=True, x_range=(3, 4), y_range=(0, 3), z_range=(0, 3))
    }


def test_size():
    assert Cube(on=True, x_range=(0, 3), y_range=(0, 3), z_range=(0, 3)).size() == 27


def test_other_merge():
    c_a = Cube(True, (0, 2), (0, 2), (0, 2))
    c_b = Cube(True, (1, 3), (1, 3), (1, 3))
    merged = merge_cubes([c_a, c_b])
    expected = {
        Cube(on=True, x_range=(0, 2), y_range=(0, 2), z_range=(0, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(1, 2), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(2, 3), z_range=(2, 3)),
        Cube(on=True, x_range=(1, 2), y_range=(2, 3), z_range=(2, 3)),
        Cube(on=True, x_range=(1, 2), y_range=(1, 2), z_range=(2, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(1, 2), z_range=(1, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(1, 2), z_range=(2, 3))
    }
    debug(merged)
    debug(len(merged))
    debug(sum(c.size() for c in merged))


def test_merge_several():
    c_a = Cube(True, (0, 3), (0, 3), (0, 3))
    c_b = Cube(True, (2, 4), (0, 4), (0, 3))
    c_c = Cube(True, (1, 5), (0, 2), (1, 2))

    assert merge_cubes([c_a, c_b, c_c]) == {
        Cube(on=True, x_range=(0, 3), y_range=(0, 3), z_range=(0, 3)),
        Cube(on=True, x_range=(3, 4), y_range=(3, 4), z_range=(0, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(3, 4), z_range=(0, 3)),
        Cube(on=True, x_range=(3, 4), y_range=(0, 3), z_range=(0, 3)),
        Cube(on=True, x_range=(4, 5), y_range=(0, 2), z_range=(1, 2))
    }


def test_remove_cube():
    c_a = Cube(True, (0, 3), (0, 3), (0, 3))
    c_b = Cube(False, (-1, 4), (1, 2), (1, 2))

    assert merge_cubes([c_a, c_b]) == {
        Cube(on=True, x_range=(0, 3), y_range=(0, 1), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 3), y_range=(0, 1), z_range=(1, 2)),
        Cube(on=True, x_range=(0, 3), y_range=(0, 1), z_range=(2, 3)),
        Cube(on=True, x_range=(0, 3), y_range=(2, 3), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 3), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(0, 3), y_range=(2, 3), z_range=(2, 3)),
        Cube(on=True, x_range=(0, 3), y_range=(1, 2), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 3), y_range=(1, 2), z_range=(2, 3))
    }


def test_cube_split_by():
    c_a = Cube(True, (1, 2), (1, 2), (1, 2))
    c_b = Cube(True, (0, 3), (0, 3), (0, 3))

    after_split = {
        Cube(on=True, x_range=(0, 1), y_range=(0, 1), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 1), y_range=(0, 1), z_range=(1, 2)),
        Cube(on=True, x_range=(0, 1), y_range=(0, 1), z_range=(2, 3)),
        Cube(on=True, x_range=(0, 1), y_range=(1, 2), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 1), y_range=(1, 2), z_range=(1, 2)),
        Cube(on=True, x_range=(0, 1), y_range=(1, 2), z_range=(2, 3)),
        Cube(on=True, x_range=(0, 1), y_range=(2, 3), z_range=(0, 1)),
        Cube(on=True, x_range=(0, 1), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(0, 1), y_range=(2, 3), z_range=(2, 3)),
        Cube(on=True, x_range=(1, 2), y_range=(0, 1), z_range=(0, 1)),
        Cube(on=True, x_range=(1, 2), y_range=(0, 1), z_range=(1, 2)),
        Cube(on=True, x_range=(1, 2), y_range=(0, 1), z_range=(2, 3)),
        Cube(on=True, x_range=(1, 2), y_range=(1, 2), z_range=(0, 1)),
        Cube(on=True, x_range=(1, 2), y_range=(1, 2), z_range=(1, 2)),
        Cube(on=True, x_range=(1, 2), y_range=(1, 2), z_range=(2, 3)),
        Cube(on=True, x_range=(1, 2), y_range=(2, 3), z_range=(0, 1)),
        Cube(on=True, x_range=(1, 2), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(1, 2), y_range=(2, 3), z_range=(2, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(0, 1), z_range=(0, 1)),
        Cube(on=True, x_range=(2, 3), y_range=(0, 1), z_range=(1, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(0, 1), z_range=(2, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(1, 2), z_range=(0, 1)),
        Cube(on=True, x_range=(2, 3), y_range=(1, 2), z_range=(1, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(1, 2), z_range=(2, 3)),
        Cube(on=True, x_range=(2, 3), y_range=(2, 3), z_range=(0, 1)),
        Cube(on=True, x_range=(2, 3), y_range=(2, 3), z_range=(1, 2)),
        Cube(on=True, x_range=(2, 3), y_range=(2, 3), z_range=(2, 3))}

    assert c_b.split_by(c_a) == after_split


def test_big_sizes():
    a = Cube.from_line("on x=-54112..-39298,y=-85059..-49293,z=-27449..7877")
    b = Cube.from_line("on x=967..23432,y=45373..81175,z=27513..53682")
    debug(a.size() + b.size() + 590784)
