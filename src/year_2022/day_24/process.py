import collections
import dataclasses
import enum


class Valley(enum.Enum):
    WALL = "#"
    GROUND = "."


class Direction(enum.Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


EXPEDITION = "E"


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


@dataclasses.dataclass(frozen=True)
class Blizzard:
    pos: Coords
    dir: Direction


OFFSET_COORDS = {
    Direction.UP: Coords(0, -1),
    Direction.DOWN: Coords(0, 1),
    Direction.LEFT: Coords(-1, 0),
    Direction.RIGHT: Coords(1, 0),
}

DECISION_COORDS = list(OFFSET_COORDS.values()) + [Coords(0, 0)]


@dataclasses.dataclass(frozen=True, kw_only=True)
class ExpeditionState:
    pos: Coords
    goal: bool = False
    goal_time: int = dataclasses.field(default=0, compare=False)
    start_again: bool = False
    start_again_time: int = dataclasses.field(default=0, compare=False)
    goal_again: bool = False
    goal_again_time: int = dataclasses.field(default=0, compare=False)


class BlizzardStates:
    def __init__(self, *args, parent):
        assert len(args) == 1
        self._states = [args[0]]
        self.pos = [{state.pos for state in self._states[0]}]
        self.parent = parent

    def _gen_next_state(self):
        previous_states = self._states[-1]
        next_states = set()
        for blizzard_state in previous_states:
            next_pos = blizzard_state.pos + OFFSET_COORDS[blizzard_state.dir]
            if next_pos in self.parent.walls:
                if blizzard_state.dir == Direction.UP:
                    next_pos = Coords(blizzard_state.pos.x, self.parent.max_y - 1)
                elif blizzard_state.dir == Direction.DOWN:
                    next_pos = Coords(blizzard_state.pos.x, self.parent.min_y + 1)
                elif blizzard_state.dir == Direction.LEFT:
                    next_pos = Coords(self.parent.max_x - 1, blizzard_state.pos.y)
                elif blizzard_state.dir == Direction.RIGHT:
                    next_pos = Coords(self.parent.min_x + 1, blizzard_state.pos.y)
                else:
                    raise Exception
            next_states.add(Blizzard(next_pos, blizzard_state.dir))
        self._states.append(next_states)
        self.pos.append({state.pos for state in self._states[-1]})

    def get_states(self, minute):
        while True:
            try:
                return self._states.__getitem__(minute)
            except IndexError:
                self._gen_next_state()

    def __getitem__(self, item):
        while True:
            try:
                return self.pos.__getitem__(item)
            except IndexError:
                self._gen_next_state()


class BlizzardBasin:
    def __init__(self, basin: str, round_trip=False) -> None:
        init_blizzard_state: set[Blizzard] = set()
        self.walls: set[Coords] = set()

        for y, row in enumerate(basin.splitlines()):
            for x, space_str in enumerate(row):
                coord = Coords(x, y)
                try:
                    space = Valley(space_str)
                except ValueError:
                    pass
                else:
                    if space == Valley.WALL:
                        self.walls.add(coord)
                    continue

                try:
                    blizzard = Direction(space_str)
                except ValueError as exc:
                    raise ValueError(
                        "space is not a valid valley space or blizzard"
                    ) from exc
                else:
                    init_blizzard_state.add(Blizzard(coord, blizzard))

        self.min_x = self._get_boundary_val(min, "x")
        self.max_x = self._get_boundary_val(max, "x")
        self.min_y = self._get_boundary_val(min, "y")
        self.max_y = self._get_boundary_val(max, "y")

        self.width = self.max_x - self.min_x - 1
        self.height = self.max_y - self.min_y - 1

        self.blizzard_states = BlizzardStates(
            init_blizzard_state,
            parent=self,
        )

        self.start = self._get_expedition_pos(self.min_y)
        self.dest = self._get_expedition_pos(self.max_y)

        self.round_trip = round_trip

        # todo confirm that all blizzards under start and dest are horizontal

    def _get_boundary_val(self, fn, axis):
        return getattr(fn(self.walls, key=lambda coord: getattr(coord, axis)), axis)

    def _get_expedition_pos(self, y_val):
        x_vals = range(self.min_x, self.max_x + 1)
        wall_x_vals = {coord.x for coord in self.walls if coord.y == y_val}
        non_wall_x_vals = set(x_vals) - wall_x_vals
        assert len(non_wall_x_vals) == 1
        (non_wall_x_val,) = non_wall_x_vals
        return Coords(non_wall_x_val, y_val)

    @classmethod
    def read_file(cls, round_trip=False) -> "BlizzardBasin":
        with open("input.txt") as f:
            return cls(f.read(), round_trip)

    def gen_map(self, minute, exp_pos: ExpeditionState | None = None):
        blizzard_state = self.blizzard_states.get_states(minute)
        blizzard_state_count = collections.Counter(
            [blizzard.pos for blizzard in blizzard_state]
        )
        single_blizzards = {
            blizzard.pos: blizzard.dir
            for blizzard in blizzard_state
            if blizzard_state_count[blizzard.pos] == 1
        }

        map_ = []
        for y in range(self.min_y, self.max_y + 1):
            row = []
            for x in range(self.min_x, self.max_x + 1):
                coord = Coords(x, y)
                if exp_pos and coord == exp_pos.pos:
                    row.append(EXPEDITION)
                elif blizzard_state_count[coord] > 1:
                    row.append(str(blizzard_state_count[coord]))
                elif coord in single_blizzards:
                    row.append(single_blizzards[coord].value)
                elif coord in self.walls:
                    row.append(Valley.WALL.value)
                else:
                    row.append(Valley.GROUND.value)
            map_.append(row)

        return "\n".join("".join(row) for row in map_)

    def __iter__(self):
        minute = 0
        seen = collections.defaultdict(set)
        seen[0].add(ExpeditionState(pos=self.start))
        states = [ExpeditionState(pos=self.start)]
        while True:
            minute += 1
            blizzard_coords = self.blizzard_states[minute]
            next_states = []
            for state in states:
                for coord in DECISION_COORDS:
                    next_coord = state.pos + coord
                    exp_state = dataclasses.replace(state, pos=next_coord)
                    if exp_state in seen[minute]:
                        continue
                    if next_coord == self.start:
                        if state.goal:
                            exp_state = dataclasses.replace(
                                state, pos=next_coord, start_again=True, start_again_time=minute
                            )
                            assert self.round_trip
                        next_states.append(exp_state)
                        seen[minute].add(exp_state)
                    elif next_coord == self.dest:
                        if state.start_again:
                            exp_state = dataclasses.replace(
                                state, pos=next_coord, goal_again=True, goal_again_time=minute
                            )
                        else:
                            exp_state = dataclasses.replace(
                                state, pos=next_coord, goal=True, goal_time=minute
                            )
                        if not self.round_trip or exp_state.goal_again:
                            return exp_state, minute
                        else:
                            next_states.append(exp_state)
                            seen[minute].add(exp_state)
                    elif (
                        (self.min_x <= next_coord.x <= self.max_x)
                        and (self.min_y <= next_coord.y <= self.max_y)
                        and next_coord not in self.walls
                        and next_coord not in blizzard_coords
                    ):
                        next_states.append(exp_state)
                        seen[minute].add(exp_state)
            yield next_states, minute
            print(minute)
            states = next_states


def main() -> None:
    bb = BlizzardBasin.read_file(round_trip=False)
    bb_it = iter(bb)
    while True:
        try:
            next(bb_it)
        except StopIteration as exc:
            _, minute = exc.value
            break

    print(f"Fewest number of minutes needed to reach goal:", minute)


    bb_2 = BlizzardBasin.read_file(round_trip=True)
    bb_2_it = iter(bb_2)
    while True:
        try:
            next(bb_2_it)
        except StopIteration as exc:
            _, minute = exc.value
            break

    print(f"Fewest number of minutes needed to reach goal with round trip:", minute)



if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
