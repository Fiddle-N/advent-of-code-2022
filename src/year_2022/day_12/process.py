import dataclasses

import networkx as nx  # type: ignore


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)


class Locations:
    START = "S"
    END = "E"


class Elevations:
    LOWEST_POINT = "a"
    HIGHEST_POINT = "z"


OFFSETS = [
    Coords(0, 1),
    Coords(1, 0),
    Coords(0, -1),
    Coords(-1, 0),
]

LOCATION_ELEVATIONS = {
    Locations.START: Elevations.LOWEST_POINT,
    Locations.END: Elevations.HIGHEST_POINT,
}


class HillClimbing:
    def __init__(self, heightmap: str) -> None:
        self._heightmap = [list(row) for row in heightmap.splitlines()]
        self._height = len(self._heightmap)
        self._width = len(self._heightmap[0])

        self._height_graph = nx.DiGraph()

        self._lowest_points = []

        for y, row in enumerate(self._heightmap):
            for x, space in enumerate(row):
                coord = Coords(x, y)

                if space == Locations.START:
                    self._start = coord
                    self._lowest_points.append(coord)
                elif space == Elevations.LOWEST_POINT:
                    self._lowest_points.append(coord)
                elif space == Locations.END:
                    self._end = coord

                neighbour_coords = self._get_neighbours(coord)
                for neighbour_coord in neighbour_coords:
                    is_valid_step = self._is_valid_step(coord, neighbour_coord)
                    if not is_valid_step:
                        continue
                    self._height_graph.add_edge(coord, neighbour_coord, weight=1)

    def _get_neighbours(self, coord: Coords) -> list[Coords]:
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if (
                0 <= neighbour_coord.x < self._width
                and 0 <= neighbour_coord.y < self._height
            ):
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def _is_valid_step(self, curr_coord: Coords, neighbour_coord: Coords) -> bool:
        curr = self._heightmap[curr_coord.y][curr_coord.x]
        neighbour = self._heightmap[neighbour_coord.y][neighbour_coord.x]

        if curr in LOCATION_ELEVATIONS:
            curr = LOCATION_ELEVATIONS[curr]

        if neighbour in LOCATION_ELEVATIONS:
            neighbour = LOCATION_ELEVATIONS[neighbour]

        return bool(
            ord(neighbour) - ord(curr) <= 1
        )  # neighbour can only be at most 1 higher than curr, and can be lower

    @classmethod
    def read_file(cls) -> 'HillClimbing':
        with open("input.txt") as f:
            return cls(f.read().strip())

    def shortest_path_length(self) -> int:
        shortest_length: int = nx.shortest_path_length(
            self._height_graph,
            source=self._start,
            target=self._end,
            weight="weight",
        )
        return shortest_length

    def shortest_path_length_from_any_elevation_a(self) -> int:
        valid_shortest_paths: list[int] = []
        for start in self._lowest_points:
            try:
                path = nx.shortest_path_length(
                    self._height_graph,
                    source=start,
                    target=self._end,
                    weight="weight",
                )
            except nx.exception.NetworkXNoPath:
                continue
            else:
                valid_shortest_paths.append(path)
        return min(valid_shortest_paths)


def main() -> None:
    hc = HillClimbing.read_file()
    print("Shortest climb:", hc.shortest_path_length())
    print(
        "Shortest climb from any lowest point:",
        hc.shortest_path_length_from_any_elevation_a(),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
