from itertools import product

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation

from utils.geometry import Point, rotate_points
from year_2021.ex_19.main import Scanner, int_rot


def test_rotations():
    input = """--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

"""
    s = Scanner.from_generator(line for line in input.split('\n'))
    for s, rot in s.rotations():
        print(int_rot(rot))
        print(s)
