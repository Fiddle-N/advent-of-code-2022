import collections
import dataclasses
import functools
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
        self.time = 30      # mins

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

    @functools.cache
    def _get_valves_left(self, valves: frozenset[str], valve: str):
        return valves.difference([valve])

    @functools.cache
    def _get_valve_pressure(self, valve: str, dist):
        if dist >= self.time:
            return None
        valve_details = self.graph[valve]
        pressure = (self.time - dist) * valve_details.flow_rate
        return pressure

    def _get_valve_pair_pressure(self, curr_valve, next_valve, dist):
        valve_details = self.graph[curr_valve]
        next_dist = valve_details.neighbours[next_valve]
        total_dist = dist + next_dist + 1  # takes one minute to open a valve
        next_pressure = self._get_valve_pressure(next_valve, total_dist)
        if next_pressure is None:
            return None, None
        return next_pressure, total_dist


    @functools.cache
    def _get_valves_pressure(self, curr_valve: str, valves: frozenset[str], dist=0):
        total_pressures = []
        for next_valve in valves:
            pressure, next_dist = self._get_valve_pair_pressure(curr_valve, next_valve, dist)
            if pressure is None:
                total_pressures.append(0)
                continue
            else:
                valves_left = self._get_valves_left(valves, next_valve)
                if valves_left:
                    future_pressure = self._get_valves_pressure(next_valve, valves_left, next_dist)
                    total_pressure = pressure + future_pressure
                else:
                    total_pressure = pressure
                total_pressures.append(total_pressure)
        return max(total_pressures)

    def get_max_pressure(self):
        valves_left = self.key_valves.difference([self.start_valve])
        return self._get_valves_pressure(self.start_valve, valves_left)


def main() -> None:
    pv = ProboscideaVolcanium.read_file()
    print(
        "Max pressure:",
        pv.get_max_pressure(),
    )
    print()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
