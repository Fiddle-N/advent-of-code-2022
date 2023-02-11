import collections
import dataclasses


@dataclasses.dataclass(frozen=True, order=True)
class MineralState:
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0




@dataclasses.dataclass(frozen=True)
class MineralRobotState:
    geode: int = 0
    obsidian: int = 0
    clay: int = 0
    ore: int = 0


class MineralSet(set[MineralState]):
    pass
    # def add(self, item):
    #     for existing in self.copy():
    #         if existing.geode <= item.geode and existing.obsidian <= item.obsidian and existing.clay <= item.clay and existing.ore <= item.ore:
    #             self.remove(existing)
    #             continue
    #     super().add(item)




def mineral_defaultdict_factory():
    return collections.defaultdict(MineralSet)


def simulate(mineral_states):
    new_mineral_states = mineral_defaultdict_factory()
    for robot_state, mineral_states in mineral_states.items():
        for mineral_state in mineral_states:
            next_ore = mineral_state.ore + robot_state.ore
            next_clay = mineral_state.clay + robot_state.clay
            next_obsidian = mineral_state.obsidian + robot_state.obsidian
            next_geode = mineral_state.geode + robot_state.geode

            next_mineral_state = MineralState(
                ore=next_ore,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,
            )

            new_mineral_states[robot_state].add(next_mineral_state)

            if mineral_state.ore >= 4:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore + 1,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode
                )

                next_mineral_state = MineralState(
                    ore=next_ore - 4,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 2:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay + 1,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 2,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 3 and mineral_state.clay >= 14:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian + 1,
                    geode=robot_state.geode
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 3,
                    clay=next_clay - 14,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 2 and mineral_state.obsidian >= 7:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode + 1
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 2,
                    clay=next_clay,
                    obsidian=next_obsidian - 7,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

    return new_mineral_states


def simulate_2(mineral_states):
    new_mineral_states = mineral_defaultdict_factory()
    for robot_state, mineral_states in mineral_states.items():
        for mineral_state in mineral_states:
            next_ore = mineral_state.ore + robot_state.ore
            next_clay = mineral_state.clay + robot_state.clay
            next_obsidian = mineral_state.obsidian + robot_state.obsidian
            next_geode = mineral_state.geode + robot_state.geode

            next_mineral_state = MineralState(
                ore=next_ore,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,
            )

            new_mineral_states[robot_state].add(next_mineral_state)

            if mineral_state.ore >= 2:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore + 1,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode
                )

                next_mineral_state = MineralState(
                    ore=next_ore - 2,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 3:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay + 1,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 3,
                    clay=next_clay,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 3 and mineral_state.clay >= 8:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian + 1,
                    geode=robot_state.geode
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 3,
                    clay=next_clay - 8,
                    obsidian=next_obsidian,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

            if mineral_state.ore >= 3 and mineral_state.obsidian >= 12:  # base calculation on original ore levels:
                next_robot_state = MineralRobotState(
                    ore=robot_state.ore,
                    clay=robot_state.clay,
                    obsidian=robot_state.obsidian,
                    geode=robot_state.geode + 1
                )
                next_mineral_state = MineralState(
                    ore=next_ore - 3,
                    clay=next_clay,
                    obsidian=next_obsidian - 12,
                    geode=next_geode,
                )

                new_mineral_states[next_robot_state].add(next_mineral_state)

    return new_mineral_states


def main():
    mineral_states = mineral_defaultdict_factory()
    mineral_states[MineralRobotState(ore=1)] = MineralSet([MineralState()])
    for _ in range(1, 25):
        # print()
        mineral_states = simulate(mineral_states)
    print('done')


    print(max(set.union(*mineral_states.values()) ).geode)




if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))