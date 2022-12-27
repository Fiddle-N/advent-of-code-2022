from typing import Any

from day_10 import process

LONG_PROGRAM = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

NOOP = process.Instr(cycle_no=1, add_val=0)


def test_crt_small_program_simulation() -> None:
    program = """\
noop
addx 3
addx -5"""

    exp_states: list[dict[str, Any]] = [
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.START),
            "instr": NOOP,
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.DURING),
            "instr": NOOP,
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.AFTER),
            "instr": None,
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=3),
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=3),
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=3),
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=3),
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=3),
            "register": 1,
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.AFTER),
            "instr": None,
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-5),
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-5),
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-5),
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-5),
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-5),
            "register": 4,
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.AFTER),
            "instr": None,
            "register": -1,
        },
    ]

    crt = process.CathodeRayTube(program)

    for _, exp_state in zip(crt, exp_states):
        assert crt.cycle == exp_state["cycle"]
        assert crt.instr == exp_state["instr"]
        assert crt.regr == exp_state["register"]


def test_crt_larger_program_simulation() -> None:
    exp_states: list[dict[str, Any]] = [
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=15),
            "register": 1,
            "screen": "",
        },
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=15),
            "register": 1,
            "screen": "#",
        },
        {
            "cycle": process.Cycle(no=1, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=15),
            "register": 1,
            "screen": "#",
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=15),
            "register": 1,
            "screen": "#",
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=15),
            "register": 1,
            "screen": "##",
        },
        {
            "cycle": process.Cycle(no=2, state=process.CycleState.AFTER),
            "instr": None,
            "register": 16,
            "screen": "##",
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-11),
            "register": 16,
            "screen": "##",
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-11),
            "register": 16,
            "screen": "##.",
        },
        {
            "cycle": process.Cycle(no=3, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-11),
            "register": 16,
            "screen": "##.",
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-11),
            "register": 16,
            "screen": "##.",
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-11),
            "register": 16,
            "screen": "##..",
        },
        {
            "cycle": process.Cycle(no=4, state=process.CycleState.AFTER),
            "instr": None,
            "register": 5,
            "screen": "##..",
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=6),
            "register": 5,
            "screen": "##..",
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=6),
            "register": 5,
            "screen": "##..#",
        },
        {
            "cycle": process.Cycle(no=5, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=6),
            "register": 5,
            "screen": "##..#",
        },
        {
            "cycle": process.Cycle(no=6, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=6),
            "register": 5,
            "screen": "##..#",
        },
        {
            "cycle": process.Cycle(no=6, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=6),
            "register": 5,
            "screen": "##..##",
        },
        {
            "cycle": process.Cycle(no=6, state=process.CycleState.AFTER),
            "instr": None,
            "register": 11,
            "screen": "##..##",
        },
        {
            "cycle": process.Cycle(no=7, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-3),
            "register": 11,
            "screen": "##..##",
        },
        {
            "cycle": process.Cycle(no=7, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-3),
            "register": 11,
            "screen": "##..##.",
        },
        {
            "cycle": process.Cycle(no=7, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-3),
            "register": 11,
            "screen": "##..##.",
        },
        {
            "cycle": process.Cycle(no=8, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-3),
            "register": 11,
            "screen": "##..##.",
        },
        {
            "cycle": process.Cycle(no=8, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-3),
            "register": 11,
            "screen": "##..##..",
        },
        {
            "cycle": process.Cycle(no=8, state=process.CycleState.AFTER),
            "instr": None,
            "register": 8,
            "screen": "##..##..",
        },
        {
            "cycle": process.Cycle(no=9, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=5),
            "register": 8,
            "screen": "##..##..",
        },
        {
            "cycle": process.Cycle(no=9, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=5),
            "register": 8,
            "screen": "##..##..#",
        },
        {
            "cycle": process.Cycle(no=9, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=5),
            "register": 8,
            "screen": "##..##..#",
        },
        {
            "cycle": process.Cycle(no=10, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=5),
            "register": 8,
            "screen": "##..##..#",
        },
        {
            "cycle": process.Cycle(no=10, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=5),
            "register": 8,
            "screen": "##..##..##",
        },
        {
            "cycle": process.Cycle(no=10, state=process.CycleState.AFTER),
            "instr": None,
            "register": 13,
            "screen": "##..##..##",
        },
        {
            "cycle": process.Cycle(no=11, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-1),
            "register": 13,
            "screen": "##..##..##",
        },
        {
            "cycle": process.Cycle(no=11, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-1),
            "register": 13,
            "screen": "##..##..##.",
        },
        {
            "cycle": process.Cycle(no=11, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 13,
            "screen": "##..##..##.",
        },
        {
            "cycle": process.Cycle(no=12, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 13,
            "screen": "##..##..##.",
        },
        {
            "cycle": process.Cycle(no=12, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 13,
            "screen": "##..##..##..",
        },
        {
            "cycle": process.Cycle(no=12, state=process.CycleState.AFTER),
            "instr": None,
            "register": 12,
            "screen": "##..##..##..",
        },
        {
            "cycle": process.Cycle(no=13, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-8),
            "register": 12,
            "screen": "##..##..##..",
        },
        {
            "cycle": process.Cycle(no=13, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-8),
            "register": 12,
            "screen": "##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=13, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-8),
            "register": 12,
            "screen": "##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=14, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-8),
            "register": 12,
            "screen": "##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=14, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-8),
            "register": 12,
            "screen": "##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=14, state=process.CycleState.AFTER),
            "instr": None,
            "register": 4,
            "screen": "##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=15, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=13),
            "register": 4,
            "screen": "##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=15, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=13),
            "register": 4,
            "screen": "##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=15, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=13),
            "register": 4,
            "screen": "##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=16, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=13),
            "register": 4,
            "screen": "##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=16, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=13),
            "register": 4,
            "screen": "##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=16, state=process.CycleState.AFTER),
            "instr": None,
            "register": 17,
            "screen": "##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=17, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=4),
            "register": 17,
            "screen": "##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=17, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=4),
            "register": 17,
            "screen": "##..##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=17, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=4),
            "register": 17,
            "screen": "##..##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=18, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=4),
            "register": 17,
            "screen": "##..##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=18, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=4),
            "register": 17,
            "screen": "##..##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=18, state=process.CycleState.AFTER),
            "instr": None,
            "register": 21,
            "screen": "##..##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=19, state=process.CycleState.START),
            "instr": NOOP,
            "register": 21,
            "screen": "##..##..##..##..##",
        },
        {
            "cycle": process.Cycle(no=19, state=process.CycleState.DURING),
            "instr": NOOP,
            "register": 21,
            "screen": "##..##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=19, state=process.CycleState.AFTER),
            "instr": None,
            "register": 21,
            "screen": "##..##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=20, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=2, add_val=-1),
            "register": 21,
            "screen": "##..##..##..##..##.",
        },
        {
            "cycle": process.Cycle(no=20, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=2, add_val=-1),
            "register": 21,
            "screen": "##..##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=20, state=process.CycleState.AFTER),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 21,
            "screen": "##..##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=21, state=process.CycleState.START),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 21,
            "screen": "##..##..##..##..##..",
        },
        {
            "cycle": process.Cycle(no=21, state=process.CycleState.DURING),
            "instr": process.Instr(cycle_no=1, add_val=-1),
            "register": 21,
            "screen": "##..##..##..##..##..#",
        },
        {
            "cycle": process.Cycle(no=21, state=process.CycleState.AFTER),
            "instr": None,
            "register": 20,
            "screen": "##..##..##..##..##..#",
        },
    ]

    crt = process.CathodeRayTube(LONG_PROGRAM)

    for _, exp_state in zip(crt, exp_states):
        assert crt.cycle == exp_state["cycle"]
        assert crt.instr == exp_state["instr"]
        assert crt.regr == exp_state["register"]
        assert crt.screen == exp_state["screen"]


def test_crt_larger_program_screen() -> None:
    crt = process.CathodeRayTube(LONG_PROGRAM)

    for _ in crt:
        pass

    assert (
        crt.screen
        == """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
    )

    crt_hc = process.CathodeRayTube(LONG_PROGRAM, high_contrast=True)

    for _ in crt_hc:
        pass

    assert (
        crt_hc.screen
        == """\
██████      ██████      ██████      ██████      ██████      ██████      ██████      ██████      ██████      ██████      
█████████         █████████         █████████         █████████         █████████         █████████         █████████   
████████████            ████████████            ████████████            ████████████            ████████████            
███████████████               ███████████████               ███████████████               ███████████████               
██████████████████                  ██████████████████                  ██████████████████                  ████████████
█████████████████████                     █████████████████████                     █████████████████████               
"""
    )


def test_crt_larger_program_signal_strengths() -> None:
    signal_strengths = {
        process.Cycle(no=20, state=process.CycleState.DURING): 420,
        process.Cycle(no=60, state=process.CycleState.DURING): 1140,
        process.Cycle(no=100, state=process.CycleState.DURING): 1800,
        process.Cycle(no=140, state=process.CycleState.DURING): 2940,
        process.Cycle(no=180, state=process.CycleState.DURING): 2880,
        process.Cycle(no=220, state=process.CycleState.DURING): 3960,
    }

    crt = process.CathodeRayTube(LONG_PROGRAM, watch_cycles=signal_strengths.keys())

    for signal_strength in crt:
        if crt.cycle in signal_strengths:
            assert signal_strengths[crt.cycle] == signal_strength

    assert crt.watched_cycles == signal_strengths

    assert sum(crt.watched_cycles.values()) == 13140
