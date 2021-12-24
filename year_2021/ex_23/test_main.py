from year_2021.ex_23.main import State, AnphType, solve_naive, FINAL_STATE_2, FINAL_STATE


def test_possible_states():
    lines = [
        "#############",
        "#...........#",
        "###B#C#B#D###",
        "  #A#D#C#A#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    s.print_debug()
    moving_b = s.get_possible_states((2, 3), AnphType.B)
    for new_s in moving_b:
        new_s.print_debug()


def test_get_moves():
    lines = [
        "#############",
        "#.B.........#",
        "###.#C#B#D###",
        "  #A#D#C#A#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    s.print_debug()
    moving_b = s.get_possible_states((1, 2), AnphType.B)
    for new_s in moving_b:
        new_s.print_debug()


def test_can_move_into_place():
    lines = [
        "#############",
        "#.A.........#",
        "###.#B#C#D###",
        "  #A#B#C#D#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    s.print_debug()
    moving_a = s.get_possible_states((1, 2), AnphType.A)
    for new_s in moving_a:
        new_s.print_debug()


def test_col_correct():
    lines = [
        "#############",
        "#.A.........#",
        "###.#B#C#D###",
        "  #A#B#C#D#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    s.print_debug()
    assert s.col_is_correct(3)
    assert s.col_is_correct(5)
    assert s.col_is_correct(7)
    assert s.col_is_correct(9)


def test_solve_easy_step():
    lines = [
        "#############",
        "#.....D.D.A.#",
        "###.#B#C#.###",
        "  #A#B#C#.#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    s.print_debug()
    solve_naive(s, FINAL_STATE, True)


def test_solve_easy_step_2():
    lines = [
        "#############",
        "#.....D.....#",
        "###.#B#C#D###",
        "  #A#B#C#A#  ",
        "  #########  ",
    ]
    s = State.from_lines(lines)
    solved = solve_naive(s, FINAL_STATE, False)
    for step in solved.chain:
        step.print_debug()
    assert solved.state.energy == 9011


def test_solve_part_2():
    lines = [
        "#############",
        "#..........D#",
        "###A#B#C#.###",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #########  "
    ]
    s = State.from_lines(lines)
    solved = solve_naive(s, FINAL_STATE_2)
    for step in solved.chain:
        step.print_debug()
    assert solved.state.energy == 3000


def test_solve_wrong_column():
    lines = [
        "#############",
        "#A....A...AA#",
        "###.#.#C#D###",
        "  #.#B#C#D#  ",
        "  #.#B#C#D#  ",
        "  #B#B#C#D#  ",
        "  #########  "
    ]
    s = State.from_lines(lines)
    solved = solve_naive(s, FINAL_STATE_2)
    for step in solved.chain:
        step.print_debug()
    assert solved.state.energy == 100


def test_solve_complex_2():
    lines = [
        "#############",
        "#...D.....AD#",
        "###.#B#C#.###",
        "  #A#B#C#.#  ",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #########  "
    ]
    s = State.from_lines(lines)
    solved = solve_naive(s, FINAL_STATE_2)
    for step in solved.chain:
        step.print_debug()
    assert solved.state.energy == 10008


def test_fast_track():
    lines = [
        "#############",
        "#.D.....A...#",
        "###.#B#C#.###",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #########  "
    ]
    s = State.from_lines(lines)
    assert solve_naive(s, FINAL_STATE_2, True) == 8006


def test_get_finished():
    lines = [
        "#############",
        "#.D.....D...#",
        "###.#B#C#.###",
        "  #A#B#C#D#  ",
        "  #A#B#C#D#  ",
        "  #A#B#C#A#  ",
        "  #########  "
    ]
    s = State.from_lines(lines)
    assert s.get_finished() == 11


def test_example_2():
    lines = """#############
#.A........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########"""
    s = State.from_lines(lines.split('\n'))
    s.print_debug()
    next_steps, _ = s.get_next_steps()
    for next_state in next_steps:
        next_state.print_debug()
    solve_naive(s, FINAL_STATE_2, False)


def test_costs():
    lines = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########"""
    s = State.from_lines(lines.split('\n'))
    # next_steps, _ = s.get_next_steps()
    # for next_state in next_steps:
    #     next_state.print_debug()
    score = 41119 + 1 * 0 + 10 * (4) + 100 * 0 + 1000 * 0
    solved = solve_naive(s, FINAL_STATE_2, False)
    for step in solved.chain:
        step.print_debug()
    assert solved.state.energy == score
