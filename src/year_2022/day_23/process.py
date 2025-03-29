import collections
import dataclasses
import enum
from collections.abc import Sequence


class Space(enum.Enum):
    ELF = "#"
    EMPTY_GROUND = "."


class Direction(enum.Enum):
    NORTH = "N"
    NORTH_EAST = "NE"
    EAST = "E"
    SOUTH_EAST = "SE"
    SOUTH = "S"
    SOUTH_WEST = "SW"
    WEST = "W"
    NORTH_WEST = "NW"


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


COORD_DIRS = {
    Direction.NORTH: Coords(0, -1),
    Direction.NORTH_EAST: Coords(1, -1),
    Direction.EAST: Coords(1, 0),
    Direction.SOUTH_EAST: Coords(1, 1),
    Direction.SOUTH: Coords(0, 1),
    Direction.SOUTH_WEST: Coords(-1, 1),
    Direction.WEST: Coords(-1, 0),
    Direction.NORTH_WEST: Coords(-1, -1),
}

DIR_PROPOSALS = {
    Direction.NORTH: (
        COORD_DIRS[Direction.NORTH],
        COORD_DIRS[Direction.NORTH_EAST],
        COORD_DIRS[Direction.NORTH_WEST],
    ),
    Direction.SOUTH: (
        COORD_DIRS[Direction.SOUTH],
        COORD_DIRS[Direction.SOUTH_EAST],
        COORD_DIRS[Direction.SOUTH_WEST],
    ),
    Direction.WEST: (
        COORD_DIRS[Direction.WEST],
        COORD_DIRS[Direction.NORTH_WEST],
        COORD_DIRS[Direction.SOUTH_WEST],
    ),
    Direction.EAST: (
        COORD_DIRS[Direction.EAST],
        COORD_DIRS[Direction.NORTH_EAST],
        COORD_DIRS[Direction.SOUTH_EAST],
    ),
}


class UnstableDiffusion:
    def __init__(self, grove):
        self.elves: set[Coords] = set()

        for y, row in enumerate(grove.splitlines()):
            for x, raw_space in enumerate(row):
                space = Space(raw_space)
                if space == Space.EMPTY_GROUND:
                    continue
                self.elves.add(Coords(x, y))

    @classmethod
    def read_file(cls) -> "UnstableDiffusion":
        with open("input.txt") as f:
            return cls(f.read())

    def _get_boundary_val(self, fn, axis):
        return getattr(fn(self.elves, key=lambda coord: getattr(coord, axis)), axis)

    @property
    def min_x(self):
        return self._get_boundary_val(min, "x")

    @property
    def max_x(self):
        return self._get_boundary_val(max, "x")

    @property
    def min_y(self):
        return self._get_boundary_val(min, "y")

    @property
    def max_y(self):
        return self._get_boundary_val(max, "y")

    def grid(self):
        return [
            [
                Space.ELF if Coords(x, y) in self.elves else Space.EMPTY_GROUND
                for x in range(self.min_x, self.max_x + 1)
            ]
            for y in range(self.min_y, self.max_y + 1)
        ]

    def __str__(self):
        return "\n".join("".join([space.value for space in row]) for row in self.grid())

    def _propose(self, elf: Coords, dirs: Sequence[Direction]) -> Direction | None:
        if not any(
            (elf + coord_dir) in self.elves for coord_dir in COORD_DIRS.values()
        ):
            return None
        for dir_ in dirs:
            offset_coords = DIR_PROPOSALS[dir_]
            neighbour_coords = [elf + offset_coord for offset_coord in offset_coords]
            if not any(
                neighbour_coord in self.elves for neighbour_coord in neighbour_coords
            ):
                return dir_
        return None

    def __iter__(self):
        dirs = collections.deque(DIR_PROPOSALS)
        round_no = 0
        while True:
            round_no += 1
            elf_proposals: dict[Coords, Direction | None] = {}
            proposal_counts = collections.Counter()
            for elf in self.elves:
                dir_proposal = self._propose(elf, dirs)
                if dir_proposal is None:
                    elf_proposals[elf] = dir_proposal
                    continue
                coord_proposal = elf + COORD_DIRS[dir_proposal]
                elf_proposals[elf] = coord_proposal
                proposal_counts[coord_proposal] += 1

            next_elves = set()
            for elf in self.elves:
                elf_proposal = elf_proposals[elf]
                elf_dest = elf_proposal if proposal_counts[elf_proposal] == 1 else elf
                next_elves.add(elf_dest)

            if self.elves == next_elves:
                return round_no
            self.elves = next_elves
            yield
            dirs.rotate(-1)

    def sum_empty_ground_tiles(self):
        return sum(
            [
                sum(tile == Space.EMPTY_GROUND for tile in row)
                for row in self.grid()
            ]
        )


def main() -> None:
    ud = UnstableDiffusion.read_file()

    initial_rounds = 10
    ud_it = iter(ud)
    for _ in range(initial_rounds):
        next(ud_it)

    print(f"No of empty ground tiles after {initial_rounds} rounds:", ud.sum_empty_ground_tiles())

    while True:
        try:
            next(ud_it)
        except StopIteration as exc:
            round_no = exc.value
            break

    print(f"Round no where no elf moves:", round_no)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
