import dataclasses
import enum
import io
import math
from typing import Callable, Iterator

import numpy as np
import numpy.typing as npt


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    TOP = enum.auto()
    BOTTOM = enum.auto()


@dataclasses.dataclass
class TreeDirectionDetails:
    view_distance: int
    is_visible: bool


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


class Tree(dict[Direction, TreeDirectionDetails]):
    def __repr__(self) -> str:
        return f"Tree({super().__repr__})"

    @property
    def is_visible(self) -> bool:
        return any(
            [direction_details.is_visible for direction_details in self.values()]
        )

    @property
    def scenic_score(self) -> int:
        return math.prod(
            [direction_details.view_distance for direction_details in self.values()]
        )


class TreetopTreeHouse:
    def __init__(self, tree_height_map: str) -> None:
        self._tree_map = self._create_tree_map(tree_height_map)
        self.trees = self._create_trees()

    @classmethod
    def read_file(cls) -> "TreetopTreeHouse":
        with open("input.txt") as f:
            return cls(f.read())

    def _create_tree_map(self, tree_height_map: str) -> npt.NDArray[np.int32]:
        f = io.StringIO(tree_height_map)
        first_line = f.readline().strip()
        f.seek(0)
        return np.genfromtxt(f, dtype="i4", delimiter=[1] * len(first_line))

    def _create_tree_details(
        self,
        current_tree_height: int,
        direction: Direction,
        directional_trees: npt.NDArray[np.int32],
    ) -> TreeDirectionDetails:
        if direction in (Direction.LEFT, Direction.TOP):
            directional_trees = np.flip(directional_trees)
        view_distance = 0
        for view_distance, tree_height in enumerate(directional_trees, start=1):
            if tree_height >= current_tree_height:
                return TreeDirectionDetails(
                    view_distance=view_distance, is_visible=False
                )
        return TreeDirectionDetails(
            view_distance=view_distance, is_visible=True
        )  # no trees can be found

    def _create_tree(self, row: int, col: int) -> Tree:
        tree_height = self._tree_map[row, col]
        directions = {
            Direction.LEFT: self._tree_map[row, :col],
            Direction.RIGHT: self._tree_map[row, col + 1 :],
            Direction.TOP: self._tree_map[:row, col],
            Direction.BOTTOM: self._tree_map[row + 1 :, col],
        }
        tree = Tree(
            {
                direction: self._create_tree_details(
                    tree_height, direction, directional_trees
                )
                for direction, directional_trees in directions.items()
            }
        )
        return tree

    def _create_trees(self) -> dict[Coords, Tree]:
        trees = {}
        tree_map_iter = np.nditer(self._tree_map, flags=["multi_index"])
        for _ in tree_map_iter:
            row, col = tree_map_iter.multi_index
            tree = self._create_tree(row, col)
            trees[Coords(col, row)] = tree
        return trees

    def _treehouse_query(self, fn: Callable[[Iterator[int]], int], query: str) -> int:
        return fn(getattr(tree, query) for tree in self.trees.values())

    def sum_visible_trees(self) -> int:
        return self._treehouse_query(sum, "is_visible")

    def max_scenic_score(self) -> int:
        return self._treehouse_query(max, "scenic_score")


def main() -> None:
    tth = TreetopTreeHouse.read_file()
    print(
        "Sum of visible trees from outside the grid:",
        tth.sum_visible_trees(),
    )
    print(
        "Highest scenic score possible for any tree:",
        tth.max_scenic_score(),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
