import pytest

from year_2021.ex_18.main_pair import Node, reduce, explode_all, split, explode


def test_explode():
    a = Node.from_str("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    explode(a)
    assert str(a) == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
    explode(a)
    assert str(a) == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    explode(a)
    assert str(a) == "[[[[0,7],4],[15,[0,13]]],[1,1]]"


def test_explode_all():
    a = Node.from_str("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    explode_all(a)
    assert str(a) == "[[[[0,7],4],[15,[0,13]]],[1,1]]"
    split(a)
    assert str(a) == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
    split(a)
    assert str(a) == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    explode_all(a)
    assert str(a) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


@pytest.mark.parametrize("test_input, expected", [
    ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
    ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
    ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
])
def test_reducer(test_input, expected):
    # p = Node.from_str(test_input)
    # p.reduce()
    # assert p == Node.from_str(expected)
    p = Node.from_str(test_input)
    reduce(p)
    assert p == Node.from_str(expected)


def test_from_str():
    a = Node(Node(Node(Node(Node(Node(value=9), Node(value=8)), Node(value=1)), Node(value=2)), Node(value=3)), Node(value=4))
    assert a == Node.from_str("[[[[[9,8],1],2],3],4]")
