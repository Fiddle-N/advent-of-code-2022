import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int

    def __add__(self, other: 'Coords') -> 'Coords':
        return Coords(self.x + other.x, self.y + other.y, self.z + other.z)


COORD_OFFSETS = [
    Coords(1, 0, 0),
    Coords(-1, 0, 0),
    Coords(0, 1, 0),
    Coords(0, -1, 0),
    Coords(0, 0, 1),
    Coords(0, 0, -1),
]


class BoilingBoulders:

    def __init__(self, droplet_input):
        self.droplet_cubes: set[Coords] = {
            Coords(*[int(val) for val in pos.split(',')])
            for pos in droplet_input.splitlines()
        }

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read())

    def calculate_surface_area(self):
        area = 0
        for droplet_cube in self.droplet_cubes:
            for offset in COORD_OFFSETS:
                neighbour = droplet_cube + offset
                if neighbour not in self.droplet_cubes:
                    area += 1
        return area

    def calculate_external_surface_area(self):
        area = 0

        start_cube = sorted(self.droplet_cubes, key=lambda coord: coord.x)[0]   # start at an example of lowest x
        start_point = start_cube + Coords(-1, 0, 0)

        seen = set()
        bfs_q = collections.deque([start_point])

        while bfs_q:
            point = bfs_q.popleft()
            if point in seen:
                continue
            neighbour_points = {point + offset for offset in COORD_OFFSETS}
            cubes = self.droplet_cubes & neighbour_points
            if not cubes:
                seen.add(point)
                continue    # we are out in open air
            area += len(cubes)
            empty_points = neighbour_points - cubes
            unseen_empty_points = {point for point in empty_points if point not in seen}
            unseen_empty_points_neighbours = set()
            for empty_point in unseen_empty_points:
                neighbour_of_neighbour_points = {empty_point + offset for offset in COORD_OFFSETS}
                empty_neighbour_of_neighbour_points = neighbour_of_neighbour_points - self.droplet_cubes
                unseen_empty_points_neighbours |= empty_neighbour_of_neighbour_points
            bfs_q.extend(unseen_empty_points)
            bfs_q.extend(unseen_empty_points_neighbours)
            seen.add(point)


        return area


def main() -> None:
    bb = BoilingBoulders.read_file()

    print(
        "Surface area of scanned lava droplet:",
        bb.calculate_surface_area(),
    )

    print(
        "External surface area of scanned lava droplet:",
        bb.calculate_external_surface_area(),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
