import pytest

from day_22 import process, process_2


def test_monkey_map_simulation_step_by_step():
    notes = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
    mm = process.MonkeyMap(notes)

    assert str(mm) == """\
        >..#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    mm_it = iter(mm)

    next(mm_it)
    assert str(mm) == """\
        >>>#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.v.    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>.    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>>....#.>>    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>v....#.>>    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>v....#.>>    
..#v...#....    
...v......#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>v....#.>>    
..#v...#....    
...>......#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>v....#.>>    
..#v...#....    
...>>>>>..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
>>>v....#.>>    
..#v...#....    
...>>>>v..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#...v..v#    
>>>v...v#.>>    
..#v...#....    
...>>>>v..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#...v..v#    
>>>v...>#.>>    
..#v...#....    
...>>>>v..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#...v..v#    
>>>v...>#.>>    
..#v...#....    
...>>>>v..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    with pytest.raises(StopIteration):
        next(mm_it)


def test_monkey_map_simulation():
    notes = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
    mm = process.MonkeyMap(notes)

    mm_it = iter(mm)

    for _ in mm_it:
        pass

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#...v..v#    
>>>v...>#.>>    
..#v...#....    
...>>>>v..#.    
        ...#....
        .....#..
        .#......
        ......#."""

    assert mm.curr_pos == process.Coords(8, 6)
    assert mm.curr_dir == process.Direction.RIGHT

    assert mm.password == 6032


def test_cube_example():
    inputs = [
        [
            [None, None, 1   , None],
            [2   , 3   , 4   , None],
            [None, None, 5   , 6   ],
        ],
        [
            [None, None, 1   ],
            [2   , 3   , 4   ],
            [None, None, 5   , 6   ],
        ],
    ]
    for input_ in inputs:
        cube = process_2.Cube(input_)
        assert cube.process() == [
            None,
            process_2.Side(
                id=1,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(6, process_2.Direction.DOWN),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(4, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(3, process_2.Direction.RIGHT),
                    process_2.Direction.UP:    process_2.OppositeEdge(2, process_2.Direction.DOWN),
                },
            ),
            process_2.Side(
                id=2,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(3, process_2.Direction.UP),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(5, process_2.Direction.DOWN),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(6, process_2.Direction.LEFT),
                    process_2.Direction.UP:    process_2.OppositeEdge(1, process_2.Direction.DOWN),
                },
            ),
            process_2.Side(
                id=3,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(4, process_2.Direction.UP),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(5, process_2.Direction.RIGHT),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(2, process_2.Direction.UP),
                    process_2.Direction.UP:    process_2.OppositeEdge(1, process_2.Direction.LEFT),
                },
            ),
            process_2.Side(
                id=4,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(6, process_2.Direction.LEFT),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(5, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(3, process_2.Direction.UP),
                    process_2.Direction.UP:    process_2.OppositeEdge(1, process_2.Direction.UP),
                },
            ),
            process_2.Side(
                id=5,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(6, process_2.Direction.UP),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(2, process_2.Direction.DOWN),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(3, process_2.Direction.LEFT),
                    process_2.Direction.UP:    process_2.OppositeEdge(4, process_2.Direction.UP),
                },
            ),
            process_2.Side(
                id=6,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(1, process_2.Direction.DOWN),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(2, process_2.Direction.RIGHT),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(5, process_2.Direction.UP),
                    process_2.Direction.UP:    process_2.OppositeEdge(4, process_2.Direction.RIGHT),
                },
            ),
        ]


def test_cube_real():
    inputs = [
        [
            [None, 1   , 2   ],
            [None, 3   , None],
            [4   , 5   , None],
            [6   , None, None],
        ],
        [
            [None, 1   , 2   ],
            [None, 3   ],
            [4   , 5   ],
            [6   ],
        ],
    ]
    for input_ in inputs:
        cube = process_2.Cube(input_)
        assert cube.process() == [
            None,
            process_2.Side(
                id=1,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(2, process_2.Direction.UP),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(3, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(4, process_2.Direction.DOWN),
                    process_2.Direction.UP:    process_2.OppositeEdge(6, process_2.Direction.LEFT),
                },
            ),
            process_2.Side(
                id=2,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(5, process_2.Direction.DOWN),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(3, process_2.Direction.LEFT),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(1, process_2.Direction.UP),
                    process_2.Direction.UP:    process_2.OppositeEdge(6, process_2.Direction.UP),
                },
            ),
            process_2.Side(
                id=3,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(2, process_2.Direction.RIGHT),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(5, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(4, process_2.Direction.RIGHT),
                    process_2.Direction.UP:    process_2.OppositeEdge(1, process_2.Direction.UP),
                },
            ),
            process_2.Side(
                id=4,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(5, process_2.Direction.UP),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(6, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(1, process_2.Direction.DOWN),
                    process_2.Direction.UP:    process_2.OppositeEdge(3, process_2.Direction.LEFT),
                },
            ),
            process_2.Side(
                id=5,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(2, process_2.Direction.DOWN),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(6, process_2.Direction.LEFT),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(4, process_2.Direction.UP),
                    process_2.Direction.UP:    process_2.OppositeEdge(3, process_2.Direction.UP),
                },
            ),
            process_2.Side(
                id=6,
                edges={
                    process_2.Direction.RIGHT: process_2.OppositeEdge(5, process_2.Direction.RIGHT),
                    process_2.Direction.DOWN:  process_2.OppositeEdge(2, process_2.Direction.UP),
                    process_2.Direction.LEFT:  process_2.OppositeEdge(1, process_2.Direction.RIGHT),
                    process_2.Direction.UP:    process_2.OppositeEdge(4, process_2.Direction.UP),
                },
            ),
        ]


def test_monkey_map_simulation_2_step_by_step():
    notes = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
    mm = process_2.MonkeyMap(notes, face_size=4)

    assert str(mm) == """\
        >..#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    mm_it = iter(mm)

    next(mm_it)
    assert str(mm) == """\
        >>>#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.v.    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)
    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>.    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>>    
..#....#....    
..........#.    
        ...#..v.
        .....#v.
        .#....v.
        ......#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>>    
..#....#....    
..........#.    
        ...#..v.
        .....#v.
        .#....<.
        ......#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>>    
..#....#....    
..........#.    
        ...#..v.
        .....#v.
        .#<<<<<.
        ......#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
........#.>>    
..#....#....    
..........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ......#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
.^......#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
.>......#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
.>>>>>>.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""

    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#......v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""


    next(mm_it)

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#..^...v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""

    with pytest.raises(StopIteration):
        next(mm_it)


def test_monkey_map_simulation_2():
    notes = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
    mm = process_2.MonkeyMap(notes, face_size=4)

    mm_it = iter(mm)

    for _ in mm_it:
        pass

    assert str(mm) == """\
        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#..^...v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#."""

    assert mm.curr_pos == process_2.Coords(7, 5)
    assert mm.curr_dir == process_2.Direction.UP

    assert mm.password == 5031