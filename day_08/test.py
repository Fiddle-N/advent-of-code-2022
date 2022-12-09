import pytest

from day_08 import process


@pytest.mark.parametrize(
    "coords, directional_assertions, overall_assertion",
    [
        # four corners - assert visible from beyond edges
        (
            process.Coords(x=0, y=0),
            (
                (process.Direction.LEFT, True),
                (process.Direction.TOP, True),
            ),
            True,
        ),
        (
            process.Coords(x=4, y=0),
            (
                (process.Direction.RIGHT, True),
                (process.Direction.TOP, True),
            ),
            True,
        ),
        (
            process.Coords(x=0, y=4),
            (
                (process.Direction.LEFT, True),
                (process.Direction.BOTTOM, True),
            ),
            True,
        ),
        (
            process.Coords(x=4, y=4),
            (
                (process.Direction.RIGHT, True),
                (process.Direction.BOTTOM, True),
            ),
            True,
        ),
        # four borders (that are not corners) - assert visible from beyond edge
        ## top
        (
            process.Coords(x=1, y=0),
            ((process.Direction.TOP, True),),
            True,
        ),
        (
            process.Coords(x=2, y=0),
            ((process.Direction.TOP, True),),
            True,
        ),
        (
            process.Coords(x=3, y=0),
            ((process.Direction.TOP, True),),
            True,
        ),
        ## bottom
        (
            process.Coords(x=1, y=4),
            ((process.Direction.BOTTOM, True),),
            True,
        ),
        (
            process.Coords(x=2, y=4),
            ((process.Direction.BOTTOM, True),),
            True,
        ),
        (
            process.Coords(x=3, y=4),
            ((process.Direction.BOTTOM, True),),
            True,
        ),
        ## left
        (
            process.Coords(x=0, y=1),
            ((process.Direction.LEFT, True),),
            True,
        ),
        (
            process.Coords(x=0, y=2),
            ((process.Direction.LEFT, True),),
            True,
        ),
        (
            process.Coords(x=0, y=3),
            ((process.Direction.LEFT, True),),
            True,
        ),
        ## right
        (
            process.Coords(x=4, y=1),
            ((process.Direction.RIGHT, True),),
            True,
        ),
        (
            process.Coords(x=4, y=2),
            ((process.Direction.RIGHT, True),),
            True,
        ),
        (
            process.Coords(x=4, y=3),
            ((process.Direction.RIGHT, True),),
            True,
        ),
        # interior nine trees
        ## top-left
        (
            process.Coords(x=1, y=1),
            (
                (process.Direction.LEFT, True),
                (process.Direction.RIGHT, False),
                (process.Direction.TOP, True),
                (process.Direction.BOTTOM, False),
            ),
            True,
        ),
        ## top-middle
        (
            process.Coords(x=2, y=1),
            (
                (process.Direction.LEFT, False),
                (process.Direction.RIGHT, True),
                (process.Direction.TOP, True),
                (process.Direction.BOTTOM, False),
            ),
            True,
        ),
        ## top-right
        (
            process.Coords(x=3, y=1),
            (
                (process.Direction.LEFT, False),
                (process.Direction.RIGHT, False),
                (process.Direction.TOP, False),
                (process.Direction.BOTTOM, False),
            ),
            False,
        ),
        ## left-middle
        (
            process.Coords(x=1, y=2),
            (
                (process.Direction.LEFT, False),
                (process.Direction.RIGHT, True),
                (process.Direction.TOP, False),
                (process.Direction.BOTTOM, False),
            ),
            True,
        ),
        ## centre
        (
            process.Coords(x=2, y=2),
            (
                (process.Direction.LEFT, False),
                (process.Direction.RIGHT, False),
                (process.Direction.TOP, False),
                (process.Direction.BOTTOM, False),
            ),
            False,
        ),
        ## right-middle
        (
            process.Coords(x=3, y=2),
            (
                (process.Direction.LEFT, False),
                (process.Direction.RIGHT, True),
                (process.Direction.TOP, False),
                (process.Direction.BOTTOM, False),
            ),
            True,
        ),
        ## bottom-left
        (
            process.Coords(x=1, y=3),
            (),
            False,
        ),
        ## bottom-middle
        (
            process.Coords(x=2, y=3),
            (),
            True,
        ),
        ## bottom-right
        (
            process.Coords(x=3, y=3),
            (),
            False,
        ),
    ],
)
def test_treetop_tree_house_is_visible(
    coords: process.Coords,
    directional_assertions: tuple[tuple[process.Direction, bool]],
    overall_assertion: bool,
) -> None:
    tree_height_map = """\
30373
25512
65332
33549
35390"""
    tth = process.TreetopTreeHouse(tree_height_map)
    tree = tth.trees[coords]
    for direction, directional_assertion in directional_assertions:
        assert tree[direction].is_visible == directional_assertion
    assert tree.is_visible == overall_assertion


def test_treetop_tree_house_sum_visible_trees() -> None:
    tree_height_map = """\
30373
25512
65332
33549
35390"""
    tth = process.TreetopTreeHouse(tree_height_map)
    assert tth.sum_visible_trees() == 21


@pytest.mark.parametrize(
    "coords, directional_assertions, overall_assertion",
    [
        (
            process.Coords(x=2, y=1),
            (
                (process.Direction.LEFT, 1),
                (process.Direction.RIGHT, 2),
                (process.Direction.TOP, 1),
                (process.Direction.BOTTOM, 2),
            ),
            4,
        ),
        (
            process.Coords(x=2, y=3),
            (
                (process.Direction.LEFT, 2),
                (process.Direction.RIGHT, 2),
                (process.Direction.TOP, 2),
                (process.Direction.BOTTOM, 1),
            ),
            8,
        ),
    ],
)
def test_treetop_tree_house_scenic_score(
    coords: process.Coords,
    directional_assertions: tuple[tuple[process.Direction, bool]],
    overall_assertion: bool,
) -> None:
    tree_height_map = """\
30373
25512
65332
33549
35390"""
    tth = process.TreetopTreeHouse(tree_height_map)
    tree = tth.trees[coords]
    for direction, directional_assertion in directional_assertions:
        assert tree[direction].view_distance == directional_assertion
    assert tree.scenic_score == overall_assertion


def test_treetop_tree_house_max_scenic_score() -> None:
    tree_height_map = """\
30373
25512
65332
33549
35390"""
    tth = process.TreetopTreeHouse(tree_height_map)
    assert tth.max_scenic_score() == 8
