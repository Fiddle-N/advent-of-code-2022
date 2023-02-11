import dataclasses
import enum
import itertools
import operator
import timeit




@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y)


class Cave(enum.Enum):
    AIR = '.'
    ROCK = '#'
    SAND_FLOWING = '~'
    SAND_SETTLED = 'o'
    SAND_SOURCE = '+'


class Directions(enum.Enum):
    DOWN = enum.auto()
    DOWN_LEFT = enum.auto()
    DOWN_RIGHT = enum.auto()


COORD_DIRECTIONS = {
    Directions.DOWN: Coords(x=0, y=1),
    Directions.DOWN_LEFT: Coords(x=-1, y=1),
    Directions.DOWN_RIGHT: Coords(x=1, y=1),
}


def read_file():
    with open('input.txt') as f:
        return f.read().strip()


class RegolithReservoir:

    def __init__(self, input_, floor=False):
        self.start = Coords(500, 0)
        self.rock = self._parse_rock_slice(input_)
        self.sand = {}
        self._curr_path = [self.start]
        self.floor = (self.max_y + 2) if floor else None

    @property
    def all_points(self):
        return {self.start} | self.rock | self.sand.keys()

    def _get_boundary(self, boundary_fn, axis):
        return getattr(boundary_fn(self.all_points, key=lambda coords: getattr(coords, axis)), axis)

    @property
    def min_x(self):
        return self._get_boundary(min, 'x')

    @property
    def max_x(self):
        return self._get_boundary(max, 'x')

    @property
    def min_y(self):
        return self._get_boundary(min, 'y')

    @property
    def max_y(self):
        max_y_boundary = self._get_boundary(max, 'y')
        try:
            floor = self.floor
        except AttributeError:
            return max_y_boundary
        else:
            if floor is None:
                return max_y_boundary
            return max(floor, max_y_boundary)

    @property
    def resting_sand(self):
        return len([coord for coord, sand_material in self.sand.items() if sand_material == Cave.SAND_SETTLED])

    @staticmethod
    def _get_coord_range(start: Coords, end: Coords) -> list[Coords]:
        x_ranges = sorted([start.x, end.x])
        y_ranges = sorted([start.y, end.y])

        is_x_equal = (x_ranges[0] == x_ranges[1])
        is_y_equal = (y_ranges[0] == y_ranges[1])

        if is_x_equal and is_y_equal:
            return [start]      # start and end is the same
        if not is_x_equal and not is_y_equal:
            raise ValueError('Start and end coords are not horizontally or vertically aligned')
        return [
            Coords(x, y)
            for x in range(x_ranges[0], x_ranges[1] + 1)
            for y in range(y_ranges[0], y_ranges[1] + 1)
        ]

    def _parse_rock_slice(self, input_: str) -> set[Coords]:
        rock = set()
        for paths in input_.splitlines():
            raw_path_points = paths.split(' -> ')
            path_points = []
            for raw_point in raw_path_points:
                raw_point_vals = raw_point.split(',')
                point_vals = [int(val) for val in raw_point_vals]
                path_points.append(Coords(*point_vals))
            for path_pair in itertools.pairwise(path_points):
                coord_range = self._get_coord_range(*path_pair)
                rock |= set(coord_range)
        return rock

    def map(self):
        min_x = self.min_x
        max_x = self.max_x
        min_y = self.min_y
        max_y = self.max_y

        map_list = []
        for y in range(min_y, max_y + 1):
            map_row = []
            for x in range(min_x, max_x + 1):
                coord = Coords(x, y)
                cave_material = self._get_cave_material(coord)
                map_row.append(cave_material.value)
            map_list.append(''.join(map_row))
        map = '\n'.join(map_list)
        return map

    def _get_cave_material(self, coord):
        if coord in self.sand:
            cave_material = self.sand[coord]
        elif coord == self.start:
            cave_material = Cave.SAND_SOURCE
        elif coord in self.rock or coord.y == self.floor:
            cave_material = Cave.ROCK
        else:
            cave_material = Cave.AIR
        return cave_material

    def _get_dest_coord(self, coord: Coords, direction:Directions) -> Coords:
        return coord + COORD_DIRECTIONS[direction]

    def __iter__(self):
        return self

    def _check_coord(self, curr_coord):
        for direction in (Directions.DOWN, Directions.DOWN_LEFT, Directions.DOWN_RIGHT):
            next_coord = self._get_dest_coord(curr_coord, direction)
            next_cave_material = self._get_cave_material(next_coord)
            if next_cave_material == Cave.AIR:
                return True, next_coord
        return False, None

    def _mark_flowing_sand(self):
        for coord in self._curr_path:
            if coord == self.start:
                continue
            self.sand[coord] = Cave.SAND_FLOWING

    def __next__(self):
        try:
            curr_coord = self._curr_path[-1]
        except IndexError as exc:
            if self.floor:
                # source has been covered up
                raise StopIteration from exc
            raise
        while True:
            is_next_coord_free, next_coord = self._check_coord(curr_coord)
            if not is_next_coord_free:
                self.sand[curr_coord] = Cave.SAND_SETTLED
                self._curr_path.pop()
                return
            self._curr_path.append(next_coord)
            if next_coord.y == self.max_y:
                # sand flows freely to bottom of cave
                self._mark_flowing_sand()
                raise StopIteration
            else:
                curr_coord = next_coord


def main():
    cave_slice_str = read_file()

    rr = RegolithReservoir(cave_slice_str)
    for _ in rr:
        pass
    print("Resting units of sand:", rr.resting_sand)

    rr2 = RegolithReservoir(cave_slice_str, floor=True)
    for _ in rr2:
        pass
    print("Resting units of sand with floor:", rr2.resting_sand)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))

