import collections
import dataclasses
import math
import functools

import parse
import sortedcontainers


@dataclasses.dataclass(frozen=True, kw_only=True)
class BaseRobot:
    ore: int
    clay: int
    obsidian: int


@dataclasses.dataclass(frozen=True, kw_only=True)
class OreRobot(BaseRobot):
    clay: int = 0
    obsidian: int = 0


@dataclasses.dataclass(frozen=True, kw_only=True)
class ClayRobot(BaseRobot):
    clay: int = 0
    obsidian: int = 0


@dataclasses.dataclass(frozen=True, kw_only=True)
class ObsidianRobot(BaseRobot):
    obsidian: int = 0


@dataclasses.dataclass(frozen=True, kw_only=True)
class GeodeRobot(BaseRobot):
    clay: int = 0


@dataclasses.dataclass(frozen=True)
class Blueprint:
    no: int
    ore: OreRobot
    clay: ClayRobot
    obsidian: ObsidianRobot
    geode: GeodeRobot


@dataclasses.dataclass(frozen=True, order=True)
class MineralState:
    geode_robots: int = 0
    obsidian_robots: int = 0
    clay_robots: int = 0
    ore_robots: int = 0
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0


class NotEnoughMaterials:

    def __init__(self, blueprint_input, line_wrapped=False):
        raw_blueprints = []
        if line_wrapped:
            blueprint_sections = blueprint_input.split('\n\n')
            for section in blueprint_sections:
                raw_blueprint = ' '.join(line.strip() for line in section.splitlines())
                raw_blueprints.append(raw_blueprint)
        else:
            raw_blueprints = blueprint_input.splitlines()
        self.blueprints = []
        for raw_blueprint in raw_blueprints:
            parse_pattern = (
                "Blueprint {no:d}: "
                "Each ore robot costs {ore_robot[ore]:d} ore. "
                "Each clay robot costs {clay_robot[ore]:d} ore. "
                "Each obsidian robot costs {obsidian_robot[ore]:d} ore and {obsidian_robot[clay]:d} clay. "
                "Each geode robot costs {geode_robot[ore]:d} ore and {geode_robot[obsidian]:d} obsidian."
            )
            parse_match = parse.parse(parse_pattern, raw_blueprint)
            self.blueprints.append(Blueprint(
                no=parse_match['no'],
                ore=OreRobot(**parse_match['ore_robot']),
                clay=ClayRobot(**parse_match['clay_robot']),
                obsidian=ObsidianRobot(**parse_match['obsidian_robot']),
                geode=GeodeRobot(**parse_match['geode_robot']),
            ))

    @classmethod
    def read_file(cls, line_wrapped=False):
        with open("input.txt") as f:
            return cls(f.read(), line_wrapped)

    @functools.cache
    def _get_robot_choices(self, blueprint, ore, clay, obsidian) -> list[str]:
        valid_robot_types = []
        for robot_type in ('ore', 'clay', 'obsidian', 'geode'):
            robot = getattr(blueprint, robot_type)
            if ore >= robot.ore and clay >= robot.clay and obsidian >= robot.obsidian:
                valid_robot_types.append(robot_type)
        return valid_robot_types

    def simulate(self, blueprint, mineral_states):
        new_mineral_states = sortedcontainers.SortedSet()

        for mineral_state in mineral_states:

            next_ore = mineral_state.ore + mineral_state.ore_robots
            next_clay = mineral_state.clay + mineral_state.clay_robots
            next_obsidian = mineral_state.obsidian + mineral_state.obsidian_robots
            next_geode = mineral_state.geode + mineral_state.geode_robots

            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,
                ore=next_ore,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,
            )

            new_mineral_states.add(next_mineral_state)

            if mineral_state.ore >= blueprint.ore.ore:  # base calculation on original ore levels:
                next_mineral_state = MineralState(
                    ore_robots=mineral_state.ore_robots + 1,
                    clay_robots=mineral_state.clay_robots,
                    obsidian_robots=mineral_state.obsidian_robots,
                    geode_robots=mineral_state.geode_robots,

                    ore=next_ore - blueprint.ore.ore,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,

                )

                new_mineral_states.add(next_mineral_state)

            if mineral_state.ore >= blueprint.clay.ore:  # base calculation on original ore levels:

                next_mineral_state = MineralState(
                    ore_robots=mineral_state.ore_robots,
                    clay_robots=mineral_state.clay_robots + 1,
                    obsidian_robots=mineral_state.obsidian_robots,
                    geode_robots=mineral_state.geode_robots,

                    ore=next_ore - blueprint.clay.ore,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,

                )

                new_mineral_states.add(next_mineral_state)

            if mineral_state.ore >= blueprint.obsidian.ore and mineral_state.clay >= blueprint.obsidian.clay:  # base calculation on original ore levels:
                next_mineral_state = MineralState(
                    ore_robots=mineral_state.ore_robots,
                    clay_robots=mineral_state.clay_robots,
                    obsidian_robots=mineral_state.obsidian_robots + 1,
                    geode_robots=mineral_state.geode_robots,

                    ore=next_ore - blueprint.obsidian.ore,
                    clay=next_clay - blueprint.obsidian.clay,
                    obsidian=next_obsidian,
                    geode=next_geode,

                )

                new_mineral_states.add(next_mineral_state)

            if mineral_state.ore >= blueprint.geode.ore and mineral_state.obsidian >= blueprint.geode.obsidian:  # base calculation on original ore levels:
                next_mineral_state = MineralState(
                    ore_robots=mineral_state.ore_robots,
                    clay_robots=mineral_state.clay_robots,
                    obsidian_robots=mineral_state.obsidian_robots,
                    geode_robots=mineral_state.geode_robots + 1,

                    ore=next_ore - blueprint.geode.ore,
                    clay=next_clay,
                    obsidian=next_obsidian - blueprint.geode.obsidian,
                    geode=next_geode,

                )

                new_mineral_states.add(next_mineral_state)

        return new_mineral_states

    def prune(self, mineral_states):
        mineral_states_q = collections.deque(mineral_states)
        new_mineral_states_q = collections.deque()

        new_mineral_states_q.append(mineral_states_q.popleft())
        while mineral_states_q:
            if not new_mineral_states_q:
                new_mineral_states_q.append(mineral_states_q.popleft())
                continue
            left = new_mineral_states_q.pop()
            right = mineral_states_q.popleft()
            if (
                    left.geode_robots <= right.geode_robots
                    and left.obsidian_robots <= right.obsidian_robots
                    and left.clay_robots <= right.clay_robots
                    and left.ore_robots <= right.ore_robots
                    and left.geode <= right.geode
                    and left.obsidian <= right.obsidian
                    and left.clay <= right.clay
                    and left.ore <= right.ore
            ):
                new_mineral_states_q.append(right)
            else:
                new_mineral_states_q.append(left)
                new_mineral_states_q.append(right)

        new_mineral_states = sortedcontainers.SortedSet(new_mineral_states_q)
        return new_mineral_states

    def find_quality_level(self, minutes=24):
        quality_levels = []
        for blueprint in self.blueprints:

            mineral_states = sortedcontainers.SortedSet()
            mineral_states.add(MineralState(ore_robots=1))

            for _ in range(minutes):
                # print(_)
                mineral_states = self.prune(mineral_states)
                mineral_states = self.simulate(blueprint, mineral_states)
            result = max(mineral_states, key=lambda x: x.geode).geode
            quality_level = blueprint.no * result
            # print(f"Blueprint id:{blueprint.no}: result:{result} quality_level:{quality_level}")
            quality_levels.append(quality_level)
        return sum(quality_levels)

    def first_three(self, minutes=32):
        quality_levels = []
        for blueprint in self.blueprints[:3]:

            mineral_states = sortedcontainers.SortedSet()
            mineral_states.add(MineralState(ore_robots=1))

            for _ in range(minutes):
                # print(_)
                mineral_states = self.prune(mineral_states)
                mineral_states = self.simulate(blueprint, mineral_states)
            result = max(mineral_states, key=lambda x: x.geode).geode
            # print()
            # print(f"Blueprint id:{blueprint.no}: result:{result}")
            quality_levels.append(result)
        return math.prod(quality_levels)


def main() -> None:
    nme = NotEnoughMaterials.read_file()

    print(
        "Total quality level:",
        nme.find_quality_level(),
    )

    print(
        "First three:",
        nme.first_three(),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))

