import pytest

from day_05 import process


def test_crate_stacks() -> None:
    crate_stacks_txt = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
"""
    crate_stacks = process.CrateStacks.from_text(crate_stacks_txt)
    assert crate_stacks == process.CrateStacks(
        [
            None,
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        ]
    )
    assert crate_stacks.end_crates == "NDP"


def test_rearrangement() -> None:
    rearrangement_txt = "move 1 from 2 to 1"
    rearrangement = process.Rearrangement.from_text(rearrangement_txt)
    assert rearrangement == process.Rearrangement(
        moves=1,
        start=2,
        end=1,
    )


def test_starting_stacks_cranemover_9000() -> None:
    input_txt = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    ss = process.SupplyStacks(input_txt, crane_type="9000")
    assert ss.crate_stacks == process.CrateStacks(
        [
            None,
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        ]
    )
    assert ss.rearrangement_proc == [
        process.Rearrangement(
            moves=1,
            start=2,
            end=1,
        ),
        process.Rearrangement(
            moves=3,
            start=1,
            end=3,
        ),
        process.Rearrangement(
            moves=2,
            start=2,
            end=1,
        ),
        process.Rearrangement(
            moves=1,
            start=1,
            end=2,
        ),
    ]
    ss_iter = iter(ss)

    exp_crate_stacks = [
        process.CrateStacks(
            [
                None,
                ["Z", "N", "D"],
                ["M", "C"],
                ["P"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                [],
                ["M", "C"],
                ["P", "D", "N", "Z"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                ["C", "M"],
                [],
                ["P", "D", "N", "Z"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                ["C"],
                ["M"],
                ["P", "D", "N", "Z"],
            ]
        )
    ]

    for exp_crate_stack in exp_crate_stacks:
        assert next(ss_iter) == exp_crate_stack

    with pytest.raises(StopIteration):
        next(ss_iter)

    assert ss.crate_stacks.end_crates == "CMZ"


def test_starting_stacks_cranemover_9001() -> None:
    input_txt = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
    ss = process.SupplyStacks(input_txt, crane_type="9001")
    assert ss.crate_stacks == process.CrateStacks(
        [
            None,
            ["Z", "N"],
            ["M", "C", "D"],
            ["P"],
        ]
    )
    assert ss.rearrangement_proc == [
        process.Rearrangement(
            moves=1,
            start=2,
            end=1,
        ),
        process.Rearrangement(
            moves=3,
            start=1,
            end=3,
        ),
        process.Rearrangement(
            moves=2,
            start=2,
            end=1,
        ),
        process.Rearrangement(
            moves=1,
            start=1,
            end=2,
        ),
    ]
    ss_iter = iter(ss)

    exp_crate_stacks = [
        process.CrateStacks(
            [
                None,
                ["Z", "N", "D"],
                ["M", "C"],
                ["P"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                [],
                ["M", "C"],
                ["P", "Z", "N", "D"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                ["M", "C"],
                [],
                ["P", "Z", "N", "D"],
            ]
        ),
        process.CrateStacks(
            [
                None,
                ["M"],
                ["C"],
                ["P", "Z", "N", "D"],
            ]
        ),
    ]

    for exp_crate_stack in exp_crate_stacks:
        assert next(ss_iter) == exp_crate_stack

    with pytest.raises(StopIteration):
        next(ss_iter)

    assert ss.crate_stacks.end_crates == "MCD"
