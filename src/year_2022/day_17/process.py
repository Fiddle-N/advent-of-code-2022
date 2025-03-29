import dataclasses
import enum
import itertools

import more_itertools


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


class Jet(enum.Enum):
    LEFT = "<"
    RIGHT = ">"


class Rock(enum.Enum):
    HORIZONTAL_LINE = enum.auto()
    PLUS = enum.auto()
    BACKWARDS_L = enum.auto()
    VERTICAL_LINE = enum.auto()
    SQUARE = enum.auto()


class Chamber(enum.Enum):
    FLOOR = "-"
    FLOOR_CORNER = "+"
    WALL = "|"
    EMPTY = "."
    FALLING_ROCK = "@"
    SETTLED_ROCK = "#"


JET_COORDS = {Jet.LEFT: Coords(-1, 0), Jet.RIGHT: Coords(1, 0)}

ROCK_COORDS = {
    Rock.HORIZONTAL_LINE: [Coords(0, 0), Coords(1, 0), Coords(2, 0), Coords(3, 0)],
    Rock.PLUS: [Coords(1, 0), Coords(0, 1), Coords(1, 1), Coords(2, 1), Coords(1, 2)],
    Rock.BACKWARDS_L: [
        Coords(0, 0),
        Coords(1, 0),
        Coords(2, 0),
        Coords(2, 1),
        Coords(2, 2),
    ],
    Rock.VERTICAL_LINE: [Coords(0, 0), Coords(0, 1), Coords(0, 2), Coords(0, 3)],
    Rock.SQUARE: [Coords(0, 0), Coords(1, 0), Coords(0, 1), Coords(1, 1)],
}

ROCK_FALL_COORD = Coords(0, -1)


class SettledRocks:
    def __init__(self):
        self._rocks = set()
        self._rocks_positional = []
        self.highest_rock_height = None

    def __repr__(self):
        return f"<SettledRocks {repr(self._rocks)}>"

    def __contains__(self, item):
        return item in self._rocks

    def add(self, rock: Coords):
        height = rock.y
        if self.highest_rock_height is None or height > self.highest_rock_height:
            self.highest_rock_height = height
        self._rocks.add(rock)
        while True:
            try:
                self._rocks_positional[rock.y].add(rock.x)
            except IndexError:
                self._rocks_positional.append(set())
            else:
                break

    def update(self, rocks: list[Coords]):
        for rock in rocks:
            self.add(rock)

    def check_for_repeating_groups(self, group_no):
        for start, _ in enumerate(self._rocks_positional):
            sublist = self._rocks_positional[start:]
            if len(sublist) < 10:
                # we are looking for large repeating groups
                # use as quick and dirty way of ditching tiny repeating groups
                return False, None, None
            if len(sublist) % group_no != 0:
                # looking for exact repeating groups so need a sublist divisible into equal parts
                continue
            groups = more_itertools.divide(group_no, sublist)
            groups = iter(groups)
            first = list(next(groups))
            if all(first == list(x) for x in groups):
                # found
                group_len = len(first)
                offset_len = len(self._rocks_positional) - group_len * group_no
                return True, group_len, offset_len
        return False, None, None




class ChamberRocks:
    def __init__(self):
        self.settled_rocks = SettledRocks()
        self.falling_rocks = []
        self.chamber_width = 7

    @property
    def highest_settled_y(self):
        if self.settled_rocks.highest_rock_height is None:
            return -1       # y=-1 represents the floor position
        return self.settled_rocks.highest_rock_height

    @property
    def highest_falling_y(self):
        return max(self.falling_rocks, key=lambda coord: coord.y).y if self.falling_rocks else 0

    @property
    def highest_y(self):
        return max(self.highest_settled_y, self.highest_falling_y)

    @property
    def tower_height(self):
        return self.highest_settled_y + 1

    def _get_chamber_space(self, coord):
        if coord in self.settled_rocks:
            return Chamber.SETTLED_ROCK
        elif coord in self.falling_rocks:
            return Chamber.FALLING_ROCK
        return Chamber.EMPTY

    def __str__(self):
        chamber_floor = [Chamber.FLOOR_CORNER] + [Chamber.FLOOR] * self.chamber_width + [Chamber.FLOOR_CORNER]
        chamber_contents = [
            [Chamber.WALL] + [self._get_chamber_space(Coords(x, y)) for x in range(self.chamber_width)] + [Chamber.WALL]
            for y in range(self.highest_y + 1)
        ]
        chamber = [chamber_floor] + chamber_contents
        return '\n'.join(reversed([
            ''.join([chamber_space.value for chamber_space in row])
            for row in chamber
        ]))

    def init_rock(self, rock: Rock):
        # left wall and floor has coordinates -1
        # add one unit to be "against the wall/floor" then add another x units for the offset
        offset = Coords(
            x=-1 + 1 + 2, y=self.highest_settled_y + 1 + 3
        )
        rock_coords = [rock_coord + offset for rock_coord in ROCK_COORDS[rock]]
        self.falling_rocks = rock_coords

    def _is_valid_lateral_move(self, rock_coord: Coords) -> bool:
        if rock_coord.x < 0 or rock_coord.x >= self.chamber_width:
            return False
        if rock_coord in self.settled_rocks:
            return False
        return True

    def _is_valid_vertical_move(self, rock_coord: Coords) -> bool:
        if rock_coord.y < 0:
            return False
        if rock_coord in self.settled_rocks:
            return False
        return True

    def move_rocks(self, move: Jet) -> None:
        putative_coords = [rock_coord + JET_COORDS[move] for rock_coord in self.falling_rocks]
        if all(self._is_valid_lateral_move(coord) for coord in putative_coords):
            self.falling_rocks = putative_coords

    def rock_fall(self) -> bool:
        putative_coords = [rock_coord + ROCK_FALL_COORD for rock_coord in self.falling_rocks]
        if did_rocks_fall := all(self._is_valid_vertical_move(coord) for coord in putative_coords):
            self.falling_rocks = putative_coords
        else:
            self.settled_rocks.update(self.falling_rocks)
            self.falling_rocks = []
        return did_rocks_fall

    def check_for_repeating_groups(self, group_no):
        return self.settled_rocks.check_for_repeating_groups(group_no)


class PyroclasticFlow:
    def __init__(self, jet_pattern, show_intermediate_states=False, yield_on_jet=False):
        self.jet_pattern = [Jet(jet) for jet in jet_pattern]
        self.show_intermediate_states = show_intermediate_states
        self.chamber_rocks = ChamberRocks()
        self.yield_on_jet = yield_on_jet

    @classmethod
    def read_file(cls, show_intermediate_states=False, yield_on_jet=False):
        with open("input.txt") as f:
            return cls(f.read().strip(), show_intermediate_states, yield_on_jet)

    def __iter__(self):
        jet_cycle = itertools.cycle(self.jet_pattern)
        rock_cycle = itertools.cycle(Rock)
        beginning_cycle = True
        curr_rock = None
        while True:
            if curr_rock is None:
                curr_rock = next(rock_cycle)
                self.chamber_rocks.init_rock(curr_rock)
                if self.show_intermediate_states or not beginning_cycle:
                    yield
                if beginning_cycle:
                    beginning_cycle = False
            jet = next(jet_cycle)
            self.chamber_rocks.move_rocks(jet)
            if self.show_intermediate_states:
                yield
            did_rocks_fall = self.chamber_rocks.rock_fall()
            if self.show_intermediate_states:
                yield
            if not did_rocks_fall:
                curr_rock = None
            if self.yield_on_jet and curr_rock:
                yield

    @property
    def tower_height(self):
        return self.chamber_rocks.tower_height

    def get_tower_height_after_large_value(self, large_value):
        found_two_groups = False
        found_three_groups = False
        number_of_rocks_after_two_groups = None
        tower_height_after_two_groups = None
        number_of_rocks_after_three_groups = None
        tower_height_after_three_groups = None
        it = iter(self)
        for count in itertools.count(start=1):
            next(it)
            found_two_groups, group_len, offset_len = self.chamber_rocks.check_for_repeating_groups(group_no=2)
            if found_two_groups:
                assert offset_len + group_len * 2 == self.tower_height
                number_of_rocks_after_two_groups = count
                tower_height_after_two_groups = self.tower_height
                break
        for count in itertools.count(start=number_of_rocks_after_two_groups + 1):
            next(it)
            if self.tower_height == (tower_height_after_two_groups + group_len):
                found_three_groups, group_len_double_check, offset_len_double_check = self.chamber_rocks.check_for_repeating_groups(group_no=3)
                if not found_three_groups:
                    continue
                assert group_len == group_len_double_check
                assert offset_len == offset_len_double_check

                number_of_rocks_after_three_groups = count
                tower_height_after_three_groups = self.tower_height

                break
            if self.tower_height > (tower_height_after_two_groups + group_len):
                raise Exception('something badly went wrong')
        rock_no_per_repeating_group = number_of_rocks_after_three_groups - number_of_rocks_after_two_groups
        rock_no_for_offset = number_of_rocks_after_three_groups - rock_no_per_repeating_group * 3

        large_value_minus_beginning_offset = large_value - rock_no_for_offset

        repeating_group_no = large_value_minus_beginning_offset // rock_no_per_repeating_group
        repeating_group_total_height = repeating_group_no * group_len

        if large_value_minus_beginning_offset % rock_no_per_repeating_group == 0:
            return repeating_group_total_height + offset_len

        rock_no_ending_offset = large_value_minus_beginning_offset - (repeating_group_no * rock_no_per_repeating_group)

        for _ in range(rock_no_ending_offset):
            next(it)

        rock_no_ending_offset_height = self.tower_height - tower_height_after_three_groups

        return repeating_group_total_height + offset_len + rock_no_ending_offset_height


def main() -> None:
    pf = PyroclasticFlow.read_file()

    pf_it = iter(pf)

    for _ in range(2022):
        next(pf_it)

    print(
        "Tower height after 2022 rocks:",
        pf.tower_height,
    )

    #

    pf2 = PyroclasticFlow.read_file()

    rock_no = 1000000000000

    print(
        f"Tower height after {rock_no} rocks:",
        pf2.get_tower_height_after_large_value(rock_no),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
