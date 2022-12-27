from day_12 import process


def test_shortest_path_from_start_to_goal() -> None:
    heightmap = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    hc = process.HillClimbing(heightmap)
    assert hc.shortest_path_length() == 31


def test_shortest_path_from_any_elevation_a_to_goal() -> None:
    heightmap = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    hc = process.HillClimbing(heightmap)
    assert hc.shortest_path_length_from_any_elevation_a() == 29


def test_shortest_path_from_any_elevation_a_to_goal_blocked_path() -> None:
    # no path from the two north lowest points, but there is a direct path from the south lowest point
    heightmap = """\
Sacccccccccccccccccccccccccc
cccccccccccccccccccccccccccc
abcdefghijklmnopqrstuvwxyzEc
cccccccccccccccccccccccccccc"""
    hc = process.HillClimbing(heightmap)
    assert hc.shortest_path_length_from_any_elevation_a() == 26
