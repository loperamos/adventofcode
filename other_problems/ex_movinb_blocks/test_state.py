from other_problems.ex_movinb_blocks.main import State
from utils.debugging import debug


def get_lines_from_str(lines):
    debug("\n")
    return [line for line in list(lines.split()) if line not in {"\n", ""}]


def test_compute_next_states():
    debug("\n")
    initial = """
2001
2001
.33.
4675
4895
"""
    s = State.from_lines(get_lines_from_str(initial))
    s.debug_board()

    for next_state in s.compute_next_states():
        next_state.debug_board()


def test_compute_next_states_two_move():
    debug("\n")
    initial = """
2001
2001
3379
46.5
48.5
"""
    s = State.from_lines(get_lines_from_str(initial))
    s.debug_board()

    for next_state in s.compute_next_states():
        next_state.debug_board()


def test_compute_next_states_cant_move():
    debug("\n")
    initial = """
2001
2001
33.9
46.5
4875
"""
    s = State.from_lines(get_lines_from_str(initial))
    s.debug_board()

    for next_state in s.compute_next_states():
        next_state.debug_board()


def test_final():
    final = """
2671
2891
.33.
4005
4005
    """
    s = State.from_lines(get_lines_from_str(final))
    s.debug_board()
    assert s.is_final()


def test_equals():
    final = """
2671
2891
.33.
4005
4005
    """
    s_a = State.from_lines(get_lines_from_str(final))
    s_b = State.from_lines(get_lines_from_str(final))
    assert s_a == s_b
    my_set = {s_a, s_b}
    assert len(my_set) == 1
