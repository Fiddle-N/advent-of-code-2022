import collections
import dataclasses
import functools
import itertools
import re


@dataclasses.dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    neighbours: dict[str:int]


class ProboscideaVolcanium:
    def __init__(self, input_: str) -> None:
        self.full_graph = {}
        for raw_valve in input_.splitlines():
            matched_valve = re.fullmatch(
                r"Valve (?P<name>\w+) has flow rate=(?P<flow_rate>\d+);"
                r" tunnels? leads? to valves? (?P<raw_neighbours>.+)",
                raw_valve,
            )
            if matched_valve is None:
                raise Exception("should've matched the valve")
            self.full_graph[name] = Valve(
                name=(name := matched_valve.group("name")),
                flow_rate=int(matched_valve.group("flow_rate")),
                neighbours={
                    neighbour: 1
                    for neighbour in matched_valve.group("raw_neighbours").split(", ")
                },  # all neighbours start out 1 away
            )
        self.key_valves = frozenset([
            valve.name
            for valve in self.full_graph.values()
            if valve.name == "AA" or valve.flow_rate != 0
        ])
        self.graph = self._prune_graph()
        self.start_valve = 'AA'
        self.time = 26      # mins

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read())

    def _node(self, valve):
        cache = {}
        q = collections.deque([(valve, 0)])
        while q:
            next_valve, dist = q.popleft()
            for neighbour in self.full_graph[next_valve].neighbours:
                if neighbour not in cache:
                    next_dist = dist + 1
                    cache[neighbour] = next_dist
                    q.append((neighbour, next_dist))
        key_nodes = {
            valve: valve_dist
            for valve, valve_dist in cache.items()
            if self.full_graph[valve].flow_rate != 0
        }
        return key_nodes

    def _prune_graph(self):
        graph = {}

        for valve in self.key_valves:
            key_nodes = self._node(valve)
            valve_details = self.full_graph[valve]
            graph[valve] = Valve(name=valve, flow_rate=valve_details.flow_rate, neighbours=key_nodes)
        return graph

    def get_max_pressure(self):
        return self._search((self.start_valve, self.start_valve,))

    def _search(self, valves: tuple[str, ...], dist=(0, 0), pressure=0):
        neighbours = self.key_valves.difference(valves)
        if not neighbours:
            return pressure

        pressures = []
        for your_neighbour, elephant_neighbour in itertools.permutations(neighbours, 2):

            curr_valves = valves[-2:]

            your_valve_details = self.graph[curr_valves[0]]
            next_your_dist = your_valve_details.neighbours[your_neighbour]
            total_your_dist = dist[0] + next_your_dist + 1       # takes one minute to oven a valve
            if total_your_dist > self.time:
                pressures.append(pressure)
                continue

            your_neighbour_details = self.graph[your_neighbour]
            next_your_pressure = (self.time - total_your_dist) * your_neighbour_details.flow_rate

            #

            ele_valve_details = self.graph[curr_valves[1]]
            next_ele_dist = ele_valve_details.neighbours[elephant_neighbour]
            total_ele_dist = dist[1] + next_ele_dist + 1  # takes one minute to oven a valve
            if total_ele_dist > self.time:
                pressures.append(pressure)
                continue

            ele_neighbour_details = self.graph[elephant_neighbour]
            next_ele_pressure = (self.time - total_ele_dist) * ele_neighbour_details.flow_rate


            total_pressure = self._search(
                valves=valves + (your_neighbour, elephant_neighbour),
                dist=(total_your_dist, total_ele_dist),
                pressure = pressure + next_your_pressure + next_ele_pressure,
            )
            pressures.append(total_pressure)
        return max(pressures) if pressures else 0

    @functools.cache
    def _get_valves_left(self, valves: frozenset[str], valves_visited: frozenset[str]) -> frozenset[str]:
        return valves - valves_visited

    @functools.cache
    def _get_valve_pressure(self, valve: str, dist):
        if dist >= self.time:
            return None
        valve_details = self.graph[valve]
        pressure = (self.time - dist) * valve_details.flow_rate
        return pressure

    @functools.cache
    def _get_valve_pair_pressure(self, curr_valve, next_valve, dist):
        valve_details = self.graph[curr_valve]
        next_dist = valve_details.neighbours[next_valve]
        total_dist = dist + next_dist + 1  # takes one minute to open a valve
        next_pressure = self._get_valve_pressure(next_valve, total_dist)
        if next_pressure is None:
            return None, self.time
        return next_pressure, total_dist

    @functools.cache
    def _get_valves_pressure(self, your_valve: str, ele_valve: str, valves: frozenset[str], your_dist=0, ele_dist=0):
        total_pressures = []

        for your_next_valve, ele_next_valve in itertools.permutations(valves, 2):

            if your_dist < self.time:
                your_pressure, your_next_dist = self._get_valve_pair_pressure(your_valve, your_next_valve, your_dist)
                your_visited_valve = your_next_valve
            else:
                your_pressure, your_next_dist = None, your_dist
                your_visited_valve = None

            if ele_dist < self.time:
                ele_pressure, ele_next_dist = self._get_valve_pair_pressure(ele_valve, ele_next_valve, ele_dist)
                ele_visited_valve = ele_next_valve
            else:
                ele_pressure, ele_next_dist = None, ele_dist
                ele_visited_valve = None

            pressures = [your_pressure, ele_pressure]
            transformed_pressures = [0 if pressure is None else pressure for pressure in pressures]

            if all(pressure is None for pressure in pressures):
                total_pressures.append(sum(transformed_pressures))
                continue
            else:
                valves_left = self._get_valves_left(valves, frozenset([your_visited_valve, ele_visited_valve]))
                if valves_left:
                    future_pressure = self._get_valves_pressure(
                        your_valve=your_visited_valve,
                        ele_valve=ele_visited_valve,
                        valves=valves_left,
                        your_dist=your_next_dist,
                        ele_dist=ele_next_dist
                    )
                    total_pressure = sum(transformed_pressures) + future_pressure
                else:
                    total_pressure = sum(transformed_pressures)
                total_pressures.append(total_pressure)
        return max(total_pressures) if total_pressures else 0

    def get_max_pressure_2(self):
        valves_left = self.key_valves.difference([self.start_valve])
        return self._get_valves_pressure(
            your_valve=self.start_valve,
            ele_valve=self.start_valve,
            valves=valves_left,
        )


def main() -> None:
    pv = ProboscideaVolcanium.read_file()
    print(
        "Max pressure:",
        pv.get_max_pressure_2(),
    )
    print(f'{pv._get_valves_left.cache_info()}')
    print(f'{pv._get_valve_pressure.cache_info()}')
    print(f'{pv._get_valve_pair_pressure.cache_info()}')
    print(f'{pv._get_valves_pressure.cache_info()}')


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))

