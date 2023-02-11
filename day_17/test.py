from day_17 import process


def test_rock_simulation_with_intermediate_stages():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=True)
    pf_it = iter(pf)

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@@@.|
|.......|
|.......|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
|.......|
|.......|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
|.......|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
|.......|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
|.......|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@@@@|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@@@.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|.@@@...|
|..@....|
|.......|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|.@@@...|
|..@....|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|.@@@...|
|..@....|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...#...|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+"""


def test_rock_simulation_without_intermediate_stages():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=False)
    pf_it = iter(pf)

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|...#...|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|..#....|
|..#....|
|####...|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@@@.|
|.......|
|.......|
|.......|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|....@..|
|....@..|
|..@@@..|
|.......|
|.......|
|.......|
|..#....|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@....|
|..@....|
|..@....|
|..@....|
|.......|
|.......|
|.......|
|.....#.|
|.....#.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@...|
|..@@...|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|....##.|
|..####.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""

    next(pf_it)
    assert str(pf.chamber_rocks) == """\
|..@@@@.|
|.......|
|.......|
|.......|
|....#..|
|....#..|
|....##.|
|##..##.|
|######.|
|.###...|
|..#....|
|.####..|
|....##.|
|....##.|
|....#..|
|..#.#..|
|..#.#..|
|#####..|
|..###..|
|...#...|
|..####.|
+-------+"""


def test_rock_simulation_after_2022_rocks():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=False)
    pf_it = iter(pf)

    for _ in range(2022):
        next(pf_it)

    assert pf.tower_height == 3068


def test_rock_simulation_after_1000000000000_rocks():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=False)

    assert pf.get_tower_height_after_large_value(1000000000000) == 1514285714288


def test_rock_simulation_after_1000000000001_rocks():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=False)

    assert pf.get_tower_height_after_large_value(1000000000001) == 1514285714289


def test_rock_simulation_after_1000000000002_rocks():
    jet_pattern = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    pf = process.PyroclasticFlow(jet_pattern, show_intermediate_states=False)

    assert pf.get_tower_height_after_large_value(1000000000002) == 1514285714292
