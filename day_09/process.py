import dataclasses
import enum
import functools
import itertools
from collections.abc import Iterator, Callable


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


class GridSpace:
    EMPTY = "."
    HEAD = "H"
    TAIL = "T"
    TAIL_HISTORY = "#"
    START = "s"


class Direction(enum.Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclasses.dataclass
class Motion:
    dir: Direction
    steps: int


class RopeKnots(list[Coords]):
    def __init__(self, seq: list[Coords]) -> None:
        super().__init__(seq)
        self.tail_history = {self[-1]}

    def __setitem__(self, key: int, value: Coords) -> None:  # type: ignore
        super().__setitem__(key, value)
        self.tail_history.add(self[-1])


class Rope:
    def __init__(self, start: Coords, knot_no: int) -> None:
        self.start = start
        self.knot_no = knot_no
        self.knots = RopeKnots([start] * self.knot_no)

    @property
    def head(self) -> Coords:
        return self.knots[0]

    @head.setter
    def head(self, val: Coords) -> None:
        self.knots[0] = val

    @property
    def tail(self) -> Coords:
        return self.knots[-1]

    @property
    def tail_history(self) -> set[Coords]:
        return self.knots.tail_history

    def __repr__(self) -> str:
        return f"<Rope knots={self.knots} head={self.head} tail={self.tail}>"

    def _is_touching_axis(
        self, left_knot: Coords, right_knot: Coords, axis: str
    ) -> bool:
        return getattr(right_knot, axis) in (
            getattr(left_knot, axis) - 1,
            getattr(left_knot, axis),
            getattr(left_knot, axis) + 1,
        )

    def _is_touching(self, left_knot: Coords, right_knot: Coords) -> bool:
        return self._is_touching_axis(
            left_knot, right_knot, axis="x"
        ) and self._is_touching_axis(left_knot, right_knot, axis="y")

    def _calc_knot_pos_axis(
        self, left_knot: Coords, right_knot: Coords, axis: str
    ) -> int:
        left_axis_val: int = getattr(left_knot, axis)
        right_axis_val: int = getattr(right_knot, axis)
        if (diff := abs(left_axis_val - right_axis_val)) <= 1:
            axis_val = left_axis_val
        elif diff == 2:
            axis_val = (left_axis_val + right_axis_val) // 2
        else:
            raise Exception("Unexpected value")
        return axis_val

    def _calc_knot_pos(self, left_knot: Coords, right_knot: Coords) -> Coords:
        new_x = self._calc_knot_pos_axis(left_knot, right_knot, axis="x")
        new_y = self._calc_knot_pos_axis(left_knot, right_knot, axis="y")
        return Coords(new_x, new_y)

    def sync_rope(self) -> None:
        knot_nos = [knot_no for knot_no, _ in enumerate(self.knots)]
        for knot_no_pair in itertools.pairwise(knot_nos):
            (left_knot_no, right_knot_no) = knot_no_pair

            left_knot = self.knots[left_knot_no]
            right_knot = self.knots[right_knot_no]

            if self._is_touching(left_knot, right_knot):
                continue

            knot_pos = self._calc_knot_pos(left_knot, right_knot)

            self.knots[right_knot_no] = knot_pos

    def _get_grid_space(self, coord: Coords, show_explicit_tail: bool) -> str:
        for knot_no, knot in enumerate(self.knots):
            if coord == knot:
                if knot_no == 0:
                    return GridSpace.HEAD
                elif show_explicit_tail and knot_no == self.knot_no - 1:
                    return GridSpace.TAIL
                else:
                    return str(knot_no)
        if coord == self.start:
            return GridSpace.START
        else:
            return GridSpace.EMPTY

    def _get_tail_history_grid_space(self, coord: Coords) -> str:
        if coord == self.start:
            return GridSpace.START
        elif coord in self.tail_history:
            return GridSpace.TAIL_HISTORY
        else:
            return GridSpace.EMPTY

    def _to_grid(
        self,
        x_start: int,
        x_end: int,
        y_start: int,
        y_end: int,
        grid_space_fn: Callable[[Coords], str],
    ) -> str:
        grid = [
            [grid_space_fn(Coords(x, y)) for x in range(x_start, x_end + 1)]
            for y in range(y_start, y_end + 1)
        ]
        return "\n".join("".join(row) for row in reversed(grid))

    def to_grid(
        self,
        x_start: int,
        x_end: int,
        y_start: int,
        y_end: int,
        show_explicit_tail: bool = False,
    ) -> str:
        grid_space_fn = functools.partial(
            self._get_grid_space, show_explicit_tail=show_explicit_tail
        )
        return self._to_grid(x_start, x_end, y_start, y_end, grid_space_fn)

    def tail_history_to_grid(
        self, x_start: int, x_end: int, y_start: int, y_end: int
    ) -> str:
        return self._to_grid(
            x_start,
            x_end,
            y_start,
            y_end,
            grid_space_fn=self._get_tail_history_grid_space,
        )


class RopeBridge:
    def __init__(
        self, motions: str, knot_no: int, yield_intermt_steps: bool = False
    ) -> None:
        self.motions = []
        for motion in motions.strip().splitlines():
            dir_, steps = motion.split()
            self.motions.append(Motion(Direction(dir_), int(steps)))

        self.rope = Rope(start=Coords(0, 0), knot_no=knot_no)
        self.yield_intermt_steps = yield_intermt_steps

    def _move_head(self, direction: Direction) -> None:
        coord_shifts = {
            Direction.UP: Coords(x=0, y=1),
            Direction.DOWN: Coords(x=0, y=-1),
            Direction.LEFT: Coords(x=-1, y=0),
            Direction.RIGHT: Coords(x=1, y=0),
        }
        self.rope.head += coord_shifts[direction]

    def __iter__(self) -> Iterator[Rope]:
        for motion in self.motions:
            for _ in range(motion.steps):
                self._move_head(motion.dir)
                self.rope.sync_rope()
                if self.yield_intermt_steps:
                    yield self.rope
            if not self.yield_intermt_steps:
                yield self.rope


def run_rb_simulator(motions: str, knot_no: int) -> None:
    rb = RopeBridge(motions, knot_no)
    for _ in iter(rb):
        pass
    print(
        f"{knot_no}-knot rope; number of positions the rope tail visits at least once:",
        len(rb.rope.tail_history),
    )


def main() -> None:
    motions = read_file()
    run_rb_simulator(motions, knot_no=2)
    run_rb_simulator(motions, knot_no=10)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
