import pytest

from day_23 import process


def test_elf_fully_surrounded_by_other_elves():
    ud = process.UnstableDiffusion("""\
#.#
.#.
#.#
""")

    ud_it = iter(ud)

    next(ud_it)
    assert str(ud) == """\
#.#
...
.#.
...
#.#"""


def test_small_example():
    ud = process.UnstableDiffusion("""\
.....
..##.
..#..
.....
..##.
.....
""")

    assert str(ud) == """\
##
#.
..
##"""

    ud_it = iter(ud)

    next(ud_it)
    assert str(ud) == """\
##
..
#.
.#
#."""

    next(ud_it)
    assert str(ud) == """\
.##.
#...
...#
....
.#.."""

    next(ud_it)
    assert str(ud) == """\
..#..
....#
#....
....#
.....
..#.."""

    with pytest.raises(StopIteration):
        next(ud_it)


def test_large_example():
    ud = process.UnstableDiffusion("""\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""")

    assert str(ud) == """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

    ud_it = iter(ud)

    next(ud_it)
    assert str(ud) == """\
.....#...
...#...#.
.#..#.#..
.....#..#
..#.#.##.
#..#.#...
#.#.#.##.
.........
..#..#..."""

    next(ud_it)
    assert str(ud) == """\
......#....
...#.....#.
..#..#.#...
......#...#
..#..#.#...
#...#.#.#..
...........
.#.#.#.##..
...#..#...."""

    next(ud_it)
    assert str(ud) == """\
......#....
....#....#.
.#..#...#..
......#...#
..#..#.#...
#..#.....#.
......##...
.##.#....#.
..#........
......#...."""

    next(ud_it)
    assert str(ud) == """\
......#....
.....#....#
.#...##....
..#.....#.#
........#..
#...###..#.
.#......#..
...##....#.
...#.......
......#...."""

    next(ud_it)
    assert str(ud) == """\
......#....
...........
.#..#.....#
........#..
.....##...#
#.#.####...
..........#
...##..#...
.#.........
.........#.
...#..#...."""

    for _ in range(5):
        next(ud_it)
    assert str(ud) == """\
......#.....
..........#.
.#.#..#.....
.....#......
..#.....#..#
#......##...
....##......
.#........#.
...#.#..#...
............
...#..#..#.."""

    assert ud.sum_empty_ground_tiles() == 110

    while True:
        try:
            next(ud_it)
        except StopIteration as exc:
            round_no = exc.value
            break

    assert str(ud) == """\
.......#......
....#......#..
..#.....#.....
......#.......
...#....#.#..#
#.............
....#.....#...
..#.....#.....
....#.#....#..
.........#....
....#......#..
.......#......"""
    assert round_no == 20
