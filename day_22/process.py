import dataclasses
import enum
import re


class Space(enum.Enum):
    TILE = '.'
    WALL = '#'
    EMPTY = ' '


class Turn(enum.Enum):
    COUNTERCLOCKWISE = 'L'
    CLOCKWISE = 'R'


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def _move(self, val):
        return Direction((self.value + val) % len(type(self)))

    def opposite(self):
        return self._move(2)

    def rotate(self, turn: Turn):
        turn_val = {
            Turn.COUNTERCLOCKWISE: -1,
            Turn.CLOCKWISE: 1,
        }[turn]
        return self._move(turn_val)


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)


DIR_STRS = {
    Direction.RIGHT: '>',
    Direction.DOWN: 'v',
    Direction.LEFT: '<',
    Direction.UP: '^',
}

DIR_COORDS = {
    Direction.RIGHT: Coords(1, 0),
    Direction.DOWN: Coords(0, 1),
    Direction.LEFT: Coords(-1, 0),
    Direction.UP: Coords(0, -1),
}


# OPP_DIRS = {
#     Direction.RIGHT: Direction.LEFT,
#     Direction.DOWN: Direction.UP,
#     Direction.LEFT: Direction.RIGHT,
#     Direction.UP: Direction.DOWN,
# }


class Map(dict):

    def _wrap(self, curr: Coords, direction: Direction):
        opp_direction = direction.opposite()
        pos = curr
        while True:
            try:
                next_pos = pos + DIR_COORDS[opp_direction]
                self[next_pos]
            except KeyError:
                return pos
            else:
                pos = next_pos

    def move(self, curr: Coords, direction:Direction):
        if curr not in self:
            return ValueError
        dest = curr + DIR_COORDS[direction]
        if dest not in self:
            dest = self._wrap(curr, direction)
        if self[dest] == Space.WALL:
            return curr
        else:
            return dest


class MonkeyMap:

    def __init__(self, notes: str) -> None:
        map_str, raw_path = notes.rstrip().split('\n\n')

        self.map = Map()

        # self.min_x = None
        # self.min_y = None
        self.max_x = None
        self.max_y = None
        for y, row in enumerate(map_str.splitlines(), start=1):
            for x, space in enumerate(row, start=1):
                map_space = Space(space)
                if map_space != Space.EMPTY:
                    self.map[Coords(x, y)] = Space(space)
                    # if self.min_x is None or x < self.min_x:
                    #     self.min_x = x
                    # if self.min_y is None or y < self.min_y:
                    #     self.min_y = y
                    if self.max_x is None or x > self.max_x:
                        self.max_x = x
                    if self.max_y is None or y > self.max_y:
                        self.max_y = y

        raw_split_path = re.findall(r'(\d+|[L|R])', raw_path)
        self.path = []
        for instr in raw_split_path:
            try:
                self.path.append(int(instr))
            except ValueError:
                self.path.append(Turn(instr))

        self.start_pos = self._find_start()
        self.start_dir = Direction.RIGHT

        self.history = {self.start_pos: self.start_dir}

    def _find_start(self):
        y_1_coords = [
            coord
            for coord in self.map
            if coord.y == 1
        ]
        return min(y_1_coords, key=lambda coord: coord.x)

    def __str__(self):
        grid = []
        for y in range(1, self.max_y + 1):
            row = []
            for x in range(1, self.max_x + 1):
                coord = Coords(x, y)
                if coord in self.history:
                    val = DIR_STRS[self.history[coord]]
                else:
                    try:
                        val = self.map[coord].value
                    except KeyError:
                        val = Space.EMPTY.value
                row.append(val)
            grid.append(row)

        return '\n'.join(
            ''.join(row)
            for row in grid
        )

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read())

    def __iter__(self):
        self.curr_pos = self.start_pos
        self.curr_dir = self.start_dir
        for instr in self.path:
            match instr:
                case int():
                    for _ in range(instr):
                        next_pos = self.map.move(self.curr_pos, self.curr_dir)
                        if self.curr_pos == next_pos:
                            break
                        else:
                            self.curr_pos = next_pos
                        self.history[self.curr_pos] = self.curr_dir
                case Turn():
                    self.curr_dir = self.curr_dir.rotate(instr)
                    self.history[self.curr_pos] = self.curr_dir
                case _:
                    raise ValueError
            yield

    @property
    def password(self):
        return sum([self.curr_pos.y * 1000, self.curr_pos.x * 4, self.curr_dir.value])


def main() -> None:
    mm = MonkeyMap.read_file()

    mm_it = iter(mm)
    for _ in mm_it:
        pass

    print("Password:", mm.password)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
