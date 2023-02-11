import collections
from collections.abc import Sequence
import dataclasses
import enum
import itertools
import re

import more_itertools


class Space(enum.Enum):
    TILE = "."
    WALL = "#"
    EMPTY = " "


class Turn(enum.Enum):
    ANTICLOCKWISE = "L"
    CLOCKWISE = "R"


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def _move(self, val):
        return Direction((self.value + val) % len(type(self)))

    def opposite(self):
        return self._move(2)

    def rotate(self, turn: Turn = Turn.CLOCKWISE):
        turn_val = {
            Turn.ANTICLOCKWISE: -1,
            Turn.CLOCKWISE: 1,
        }[turn]
        return self._move(turn_val)


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


DIR_STRS = {
    Direction.RIGHT: ">",
    Direction.DOWN: "v",
    Direction.LEFT: "<",
    Direction.UP: "^",
}

DIR_COORDS = {
    Direction.RIGHT: Coords(1, 0),
    Direction.DOWN: Coords(0, 1),
    Direction.LEFT: Coords(-1, 0),
    Direction.UP: Coords(0, -1),
}


@dataclasses.dataclass(frozen=True)
class BaseEdge:
    id: int
    dir: Direction


class Edge(BaseEdge):
    pass


class OppositeEdge(BaseEdge):
    pass


@dataclasses.dataclass
class Side:
    id: int
    edges: dict[Direction, OppositeEdge] = dataclasses.field(
        default_factory=dict, repr=False
    )


@dataclasses.dataclass
class SideCoords:
    id: int
    edges: dict[Direction, Sequence[Coords]] = dataclasses.field(
        default_factory=dict, repr=False
    )


@dataclasses.dataclass
class CoordPos:
    next_pos: int
    next_face: int
    next_edge_dir: Direction




class Cube:
    def __init__(self, input_: list[list[int | None]]):
        self.sides = {}
        self.side_list: list[Side | None] = [None] * 7
        for y, row in enumerate(input_):
            for x, id_ in enumerate(row):
                if id_ is not None:
                    side = Side(id_)
                    self.sides[Coords(x, y)] = side
                    self.side_list[side.id] = side

    def _determine_up_neighbours(self):
        for coord, side in self.sides.items():
            for dir, dir_coord in DIR_COORDS.items():
                neighbour = coord + dir_coord
                if neighbour in self.sides:
                    neighbour_side = self.sides[neighbour]
                    self.sides[coord].edges[dir] = OppositeEdge(
                        neighbour_side.id, Direction.UP
                    )

    def _get_corners(self):
        corners = []
        dir_pairs = itertools.pairwise(list(Direction) + [list(Direction)[0]])
        for pair in dir_pairs:
            for coord, side in self.sides.items():
                if all(dir_ in side.edges for dir_ in pair) and all(
                    side.edges[dir_].dir == Direction.UP for dir_ in pair
                ):
                    corners.append((coord, *pair))
        return corners

    def _get_sides_for_dir(self, coord, dir_):
        sides = []
        curr_coord = coord
        while True:
            next_coord = curr_coord + DIR_COORDS[dir_]
            if next_coord not in self.sides:
                break
            else:
                sides.append(self.sides[next_coord])
                curr_coord = next_coord
        return sides

    @staticmethod
    def _determine_corner_neighbours_one_way(edge_dir, sides, other_sides, rotation):
        side_orientation = Direction.UP
        side_pairs = itertools.product(sides, other_sides)
        pair_0 = next(side_pairs)

        side_orientation = side_orientation.rotate(rotation)
        pair_0[1].edges[edge_dir] = OppositeEdge(pair_0[0].id, side_orientation)

        try:
            pair_1 = next(side_pairs)
        except StopIteration:
            return

        side_orientation = side_orientation.rotate(rotation)
        if pair_1[0] != pair_0[0]:
            edge_dir = edge_dir.rotate(rotation)
        else:
            edge_dir = edge_dir
        pair_1[1].edges[edge_dir] = OppositeEdge(pair_1[0].id, side_orientation)

    def _determine_corner_neighbours(self, side_coord, dir_0, dir_1):
        dir_0_sides = self._get_sides_for_dir(side_coord, dir_0)
        dir_1_sides = self._get_sides_for_dir(side_coord, dir_1)

        assert {len(dir_0_sides), len(dir_1_sides)} in ({1}, {1, 2})

        self._determine_corner_neighbours_one_way(
            dir_0, dir_0_sides, dir_1_sides, rotation=Turn.CLOCKWISE
        )
        self._determine_corner_neighbours_one_way(
            dir_1, dir_1_sides, dir_0_sides, rotation=Turn.ANTICLOCKWISE
        )

    def _determine_corners_neighbours(self, corners):
        for side_coord, dir_0, dir_1 in corners:
            self._determine_corner_neighbours(side_coord, dir_0, dir_1)

    def _get_unmatched_edges(self):
        unmatched_edges = []
        for side in self.sides.values():
            for direction in list(Direction):
                if direction not in side.edges:
                    unmatched_edges.append(Edge(side.id, direction))
        return unmatched_edges

    def _pair_unmatched_edges_single_pair_one_way(self, edge, other_edge):
        side = self.side_list[edge.id]

        side_dir = Direction.UP
        other_edge_match_dir = other_edge.dir

        while True:
            if other_edge_match_dir == edge.dir.opposite():
                side.edges[edge.dir] = OppositeEdge(id=other_edge.id, dir=side_dir)
                break
            side_dir = side_dir.rotate()
            other_edge_match_dir = other_edge_match_dir.rotate()

    def _pair_unmatched_edges_single_pair(self, unmatched_edges):
        edge_0, edge_1 = unmatched_edges

        self._pair_unmatched_edges_single_pair_one_way(edge_0, edge_1)
        self._pair_unmatched_edges_single_pair_one_way(edge_1, edge_0)

    def _pair_unmatched_edges_double_pair(self, unmatched_edges):
        side_ids = {edge.id for edge in unmatched_edges}
        neighbouring_edges: dict[Edge, list[int]] = {}
        for edge in unmatched_edges:
            side = self.side_list[edge.id]
            neighbouring_dirs = [
                edge.dir.rotate(turn) for turn in (Turn.ANTICLOCKWISE, Turn.CLOCKWISE)
            ]
            neighbouring_edge_ids = []
            for dir_ in neighbouring_dirs:
                if dir_ in side.edges:
                    neighbouring_edge_id = side.edges[dir_].id
                    if neighbouring_edge_id not in side_ids:
                        neighbouring_edge_ids.append(neighbouring_edge_id)
            neighbouring_edges[edge] = neighbouring_edge_ids

        collated_edge_dict = collections.defaultdict(list)
        for neighbour_edge, neighbours in neighbouring_edges.items():
            assert len(neighbours) == 1
            (neighbour,) = neighbours
            collated_edge_dict[neighbour].append(neighbour_edge)

        for edge_pair in collated_edge_dict.values():
            assert len(edge_pair) == 2
            self._pair_unmatched_edges_single_pair(edge_pair)

    def process(self):
        self._determine_up_neighbours()

        corners = self._get_corners()
        assert len(corners) == 3
        self._determine_corners_neighbours(corners)

        unmatched_edges = self._get_unmatched_edges()
        assert len(unmatched_edges) in (2, 4)
        if len(unmatched_edges) == 2:
            self._pair_unmatched_edges_single_pair(unmatched_edges)
        elif len(unmatched_edges) == 4:
            self._pair_unmatched_edges_double_pair(unmatched_edges)
        else:
            raise Exception("Unexpected situation")

        return self.side_list


class Map(dict):
    def __init__(self, cube_edges, cube_edge_coords, cube_coord_edges, *args, **kwargs):
        self.cube_edges = cube_edges
        self.cube_edge_coords = cube_edge_coords
        self.cube_coord_edges = cube_coord_edges
        super().__init__(*args, **kwargs)

    def _wrap(self, curr: Coords, direction: Direction):
        edge_details = self.cube_coord_edges[curr][direction]
        dest = self.cube_edge_coords[edge_details.next_face].edges[edge_details.next_edge_dir][edge_details.next_pos]
        next_dir = edge_details.next_edge_dir.opposite()
        return dest, next_dir

    def move(self, curr: Coords, direction: Direction):
        if curr not in self:
            return ValueError
        dest = curr + DIR_COORDS[direction]
        dest_direction = direction
        if dest not in self:
            dest, dest_direction = self._wrap(curr, direction)
        if self[dest] == Space.WALL:
            return curr, direction
        else:
            return dest, dest_direction


class MonkeyMap:
    def __init__(self, notes: str, face_size: int) -> None:
        self.face_size = face_size
        map_str, raw_path = notes.rstrip().split("\n\n")

        self.cube_edge_coords = [None]

        face_no = 0
        cube_input = []
        for face_row_details in more_itertools.chunked(
            zip(itertools.count(1), map_str.splitlines()), face_size, strict=True
        ):
            cube_row = []
            y_vals, face_row = zip(*face_row_details)
            inverse_face_row = zip(*face_row)
            for inverse_face_details in more_itertools.chunked(
                zip(itertools.count(1), inverse_face_row), face_size, strict=True
            ):
                x_vals, inverse_face = zip(*inverse_face_details)
                face = list(zip(*inverse_face))

                face_set = set.union(*[set(face_line) for face_line in face])
                assert face_set in (
                    {Space.EMPTY.value},
                    {Space.TILE.value, Space.WALL.value},
                )

                is_cube_face = False
                if face_set == {Space.EMPTY.value}:
                    cube_row.append(None)
                else:
                    is_cube_face = True
                    face_no += 1
                    cube_row.append(face_no)

                if not is_cube_face:
                    continue

                face_coords = [[Coords(x, y) for x in x_vals] for y in y_vals]

                inverse_face_coords = list(zip(*face_coords))
                side_coords = SideCoords(
                    id=face_no,
                    edges={
                        Direction.RIGHT: inverse_face_coords[-1],
                        Direction.DOWN: face_coords[-1][::-1],
                        Direction.LEFT: inverse_face_coords[0][::-1],
                        Direction.UP: face_coords[0],
                    },
                )
                self.cube_edge_coords.append(side_coords)

            cube_input.append(cube_row)

        cube = Cube(cube_input)
        self.cube_edges = cube.process()

        self.cube_coord_edges = collections.defaultdict(dict)
        for side in self.cube_edge_coords:
            if side is None:
                continue
            for direction, coords in side.edges.items():
                edge = self.cube_edges[side.id].edges[direction]
                opposite_edge_dir = [dir_ for dir_, opp_edge in self.cube_edges[edge.id].edges.items() if opp_edge.id == side.id]
                assert len(opposite_edge_dir) == 1
                opposite_edge_dir, = opposite_edge_dir
                for idx, coord in enumerate(coords):
                    self.cube_coord_edges[coord][direction] = CoordPos(
                        next_pos=(self.face_size - idx) - 1,
                        next_face=edge.id,
                        next_edge_dir=opposite_edge_dir,
                    )

        self.map = Map(
            cube_edges=self.cube_edges,
            cube_edge_coords=self.cube_edge_coords,
            cube_coord_edges=self.cube_coord_edges,
        )

        # TODO integrate with above code
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

        raw_split_path = re.findall(r"(\d+|[L|R])", raw_path)
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
        y_1_coords = [coord for coord in self.map if coord.y == 1]
        return min(y_1_coords, key=lambda coord: coord.x)

    @classmethod
    def read_file(cls, face_size: int):
        with open("input.txt") as f:
            return cls(f.read(), face_size)

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

        return "\n".join("".join(row) for row in grid)

    def __iter__(self):
        self.curr_pos = self.start_pos
        self.curr_dir = self.start_dir
        for instr in self.path:
            match instr:
                case int():
                    for _ in range(instr):
                        next_pos, next_dir = self.map.move(self.curr_pos, self.curr_dir)
                        if self.curr_pos == next_pos:
                            break
                        else:
                            self.curr_pos = next_pos
                            self.curr_dir = next_dir
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
    mm = MonkeyMap.read_file(face_size=50)

    mm_it = iter(mm)
    for _ in mm_it:
        pass

    print("Password:", mm.password)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
