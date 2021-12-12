from utils.debugging import i, df
from year_2021.utils.geometry import Point


def test_create_point():
    p_1 = Point.from_vals(0, 1, 5, 6, 3)
    p_2 = Point.from_vals(0, 1, 5, 6, 3)
    df(p_1 + p_2)
    df(p_1 * 2)
