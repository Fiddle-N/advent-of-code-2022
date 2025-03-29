import pytest

from day_14 import process


class TestMapGeneration:

    def test_map_gen(self):
        input_ = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
        rr = process.RegolithReservoir(input_)
        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

    def test_map_gen_with_floor(self):
        input_ = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
        rr = process.RegolithReservoir(input_, floor=True)
        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########.
..........
##########"""
        act_map = rr.map()
        assert act_map == exp_map


class TestRegolithReservoir:

    def test_simple_example(self):
        input_ = """\
498,4 -> 502,4
"""
        rr = process.RegolithReservoir(input_)

        exp_map = """\
..+..
.....
.....
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        rr_it = iter(rr)

        next(rr_it)
        exp_map = """\
..+..
.....
.....
..o..
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
..+..
.....
.....
.oo..
#####"""
        act_map = rr.map()
        assert act_map == exp_map


        next(rr_it)
        exp_map = """\
..+..
.....
.....
.ooo.
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
..+..
.....
..o..
.ooo.
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        with pytest.raises(StopIteration):
            next(rr_it)

        exp_map = """\
...+..
...~..
..~o..
.~ooo.
~#####"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_complex_example(self):
        input_ = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
        rr = process.RegolithReservoir(input_)

        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        rr_it = iter(rr)

        next(rr_it)
        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        for _ in range(3):
            next(rr_it)

        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        for _ in range(17):
            next(rr_it)

        exp_map = """\
......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        for _ in range(2):
            next(rr_it)

        exp_map = """\
......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########."""
        act_map = rr.map()
        assert act_map == exp_map

        with pytest.raises(StopIteration):
            next(rr_it)

        exp_map = """\
.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########."""      # todo show flowing sand forever
        act_map = rr.map()
        assert act_map == exp_map

        assert rr.resting_sand == 24


class TestRegolithReservoirWithFloor:

    def test_simple_example(self):
        input_ = """\
498,4 -> 502,4
"""
        rr = process.RegolithReservoir(input_, floor=True)

        exp_map = """\
..+..
.....
.....
.....
#####
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        rr_it = iter(rr)

        next(rr_it)
        exp_map = """\
..+..
.....
.....
..o..
#####
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
..+..
.....
.....
.oo..
#####
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map


        next(rr_it)
        exp_map = """\
..+..
.....
.....
.ooo.
#####
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
..+..
.....
..o..
.ooo.
#####
.....
#####"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
...+..
......
...o..
..ooo.
.#####
o.....
######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+..
.......
....o..
...ooo.
..#####
oo.....
#######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+..
.......
....o..
...ooo.
..#####
ooo....
#######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+..
.......
....o..
...ooo.
.o#####
ooo....
#######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+..
.......
....o..
..oooo.
.o#####
ooo....
#######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+..
.......
...oo..
..oooo.
.o#####
ooo....
#######"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+...
........
...oo...
..oooo..
.o#####.
ooo....o
########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+...
........
...oo...
..oooo..
.o#####.
ooo...oo
########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+....
.........
...oo....
..oooo...
.o#####..
ooo...ooo
#########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+....
.........
...oo....
..oooo...
.o#####o.
ooo...ooo
#########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+....
.........
...oo....
..ooooo..
.o#####o.
ooo...ooo
#########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+....
.........
...ooo...
..ooooo..
.o#####o.
ooo...ooo
#########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
....+....
....o....
...ooo...
..ooooo..
.o#####o.
ooo...ooo
#########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+....
.....o....
....ooo...
...ooooo..
..o#####o.
oooo...ooo
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+....
.....o....
....ooo...
...ooooo..
.oo#####o.
oooo...ooo
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+....
.....o....
....ooo...
..oooooo..
.oo#####o.
oooo...ooo
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+....
.....o....
...oooo...
..oooooo..
.oo#####o.
oooo...ooo
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+....
....oo....
...oooo...
..oooooo..
.oo#####o.
oooo...ooo
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+.....
....oo.....
...oooo....
..oooooo...
.oo#####o..
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+.....
....oo.....
...oooo....
..oooooo...
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+.....
....oo.....
...oooo....
..ooooooo..
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+.....
....oo.....
...ooooo...
..ooooooo..
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....+.....
....ooo....
...ooooo...
..ooooooo..
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        next(rr_it)
        exp_map = """\
.....o.....
....ooo....
...ooooo...
..ooooooo..
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

        with pytest.raises(StopIteration):
            next(rr_it)

        exp_map = """\
.....o.....
....ooo....
...ooooo...
..ooooooo..
.oo#####oo.
oooo...oooo
###########"""
        act_map = rr.map()
        assert act_map == exp_map

    def test_complex_example(self):
        input_ = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
        rr = process.RegolithReservoir(input_, floor=True)

        exp_map = """\
......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########.
..........
##########"""
        act_map = rr.map()
        assert act_map == exp_map

        rr_it = iter(rr)

        for _ in rr_it:
            pass

        exp_map = """\
..........o..........
.........ooo.........
........ooooo........
.......ooooooo.......
......oo#ooo##o......
.....ooo#ooo#ooo.....
....oo###ooo#oooo....
...oooo.oooo#ooooo...
..oooooooooo#oooooo..
.ooo#########ooooooo.
ooooo.......ooooooooo
#####################"""
        act_map = rr.map()
        assert act_map == exp_map

        assert rr.resting_sand == 93

