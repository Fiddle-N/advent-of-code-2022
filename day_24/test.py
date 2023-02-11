from day_24 import process


def test_blizzard_basin_simple_map():
    bb = process.BlizzardBasin("""\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""")

    assert bb.gen_map(0) == """\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

    assert bb.gen_map(1) == """\
#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#"""

    assert bb.gen_map(2) == """\
#.#####
#...v.#
#..>..#
#.....#
#.....#
#.....#
#####.#"""

    assert bb.gen_map(3) == """\
#.#####
#.....#
#...2.#
#.....#
#.....#
#.....#
#####.#"""

    assert bb.gen_map(4) == """\
#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#"""

    assert bb.gen_map(4) == """\
#.#####
#.....#
#....>#
#...v.#
#.....#
#.....#
#####.#"""

    assert bb.gen_map(5) == """\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""


def test_blizzard_basin_complex_map():
    bb = process.BlizzardBasin("""\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""")
    bb_it = iter(bb)

    states, minute = next(bb_it)

    exp = """\
#.######
#E>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.2>2..#
#E^22^<#
#.>2.^>#
#.>..<.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#<^<22.#
#E2<.2.#
#><2>..#
#..><..#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#E<..22#
#<<.<..#
#<2.>>.#
#.^22^.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#2Ev.<>#
#<.<..<#
#.^>^22#
#.2..2.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#>2E<.<#
#.2v^2<#
#>..>2>#
#<....>#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.22^2.#
#<vE<2.#
#>>v<>.#
#>....<#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.<>2^.#
#.E<<.<#
#.22..>#
#.2v^2.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#<E2>>.#
#.<<.<.#
#>2>2^.#
#.v><^.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.2E.>2#
#<2v2^.#
#<>.>2.#
#..<>..#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#2^E^2>#
#<v<.^<#
#..2.>2#
#.<..>.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#>>.<^<#
#.<E.<<#
#>v.><>#
#<^v^^>#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.>3.<.#
#<..<<.#
#>2E22.#
#>v..^<#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.2>2..#
#.^22^<#
#.>2E^>#
#.>..<.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#<^<22.#
#.2<.2.#
#><2>E.#
#..><..#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#.<..22#
#<<.<..#
#<2.>>E#
#.^22^.#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    states, minute = next(bb_it)

    exp = """\
#.######
#2.v.<>#
#<.<..<#
#.^>^22#
#.2..2E#
######.#"""
    assert any(
        bb.gen_map(minute=minute, exp_pos=state) == exp
        for state in states
    )

    try:
        next(bb_it)
    except StopIteration as exc:
        state, minute = exc.value
    else:
        state = None

    exp = """\
#.######
#>2.<.<#
#.2v^2<#
#>..>2>#
#<....>#
######E#"""

    assert bb.gen_map(minute=minute, exp_pos=state) == exp
    assert minute == 18


def test_blizzard_basin_complex_map_round_trip():
    bb = process.BlizzardBasin("""\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""", round_trip=True)
    bb_it = iter(bb)

    while True:
        try:
            next(bb_it)
        except StopIteration as exc:
            state, minute = exc.value
            break

    assert state.goal_again_time == 54


def test_blizzard_basin_waiting_at_start():
    bb = process.BlizzardBasin("""\
#.#####
#.<...#
#.....#
#.....#
#.....#
#.....#
#####.#
""")
    bb_it = iter(bb)

    while True:
        try:
            next(bb_it)
        except StopIteration as exc:
            state, minute = exc.value
            break

    assert minute == 11

# todo waiting at end