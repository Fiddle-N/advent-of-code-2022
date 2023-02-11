import collections
import dataclasses

import sortedcontainers


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


def simulate(mineral_states):
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

        if mineral_state.ore >= 4:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots + 1,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 4,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 2:  # base calculation on original ore levels:

            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots + 1,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 2,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3 and mineral_state.clay >= 14:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots + 1,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 3,
                clay=next_clay - 14,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 2 and mineral_state.obsidian >= 7:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots + 1,

                ore=next_ore - 2,
                clay=next_clay,
                obsidian=next_obsidian - 7,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

    return new_mineral_states


def simulate_2(mineral_states):
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

        if mineral_state.ore >= 2:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots + 1,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 2,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3:  # base calculation on original ore levels:

            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots + 1,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 3,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3 and mineral_state.clay >= 8:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots + 1,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 3,
                clay=next_clay - 8,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3 and mineral_state.obsidian >= 12:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots + 1,

                ore=next_ore - 3,
                clay=next_clay,
                obsidian=next_obsidian - 12,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

    return new_mineral_states

def simulate_3(mineral_states):
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

        if mineral_state.ore >= 4:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots + 1,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 4,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3:  # base calculation on original ore levels:

            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots + 1,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 3,
                clay=next_clay,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3 and mineral_state.clay >= 7:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots + 1,
                geode_robots=mineral_state.geode_robots,

                ore=next_ore - 3,
                clay=next_clay - 7,
                obsidian=next_obsidian,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

        if mineral_state.ore >= 3 and mineral_state.obsidian >= 9:  # base calculation on original ore levels:
            next_mineral_state = MineralState(
                ore_robots=mineral_state.ore_robots,
                clay_robots=mineral_state.clay_robots,
                obsidian_robots=mineral_state.obsidian_robots,
                geode_robots=mineral_state.geode_robots + 1,

                ore=next_ore - 3,
                clay=next_clay,
                obsidian=next_obsidian - 9,
                geode=next_geode,

            )

            new_mineral_states.add(next_mineral_state)

    return new_mineral_states


def prune(mineral_states):
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


def main():
    mineral_states = sortedcontainers.SortedSet()
    mineral_states.add(MineralState(ore_robots=1))
    for _ in range(1, 33):
        print(_)
        mineral_states = prune(mineral_states)
        mineral_states = simulate(mineral_states)
    print('done')
    print(max(mineral_states, key=lambda x: x.geode).geode)


    # print(max(set.union(*mineral_states.values()) ).geode)




if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))