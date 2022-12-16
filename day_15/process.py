import dataclasses
import operator
import parse    # type: ignore
from typing import Callable


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def distance(self, other: "Coords") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclasses.dataclass
class Reading:
    sensor: Coords
    beacon: Coords
    distance: int = dataclasses.field(init=False)
    sensor_min_x: int = dataclasses.field(init=False, repr=False)
    sensor_min_y: int = dataclasses.field(init=False, repr=False)
    sensor_max_x: int = dataclasses.field(init=False, repr=False)
    sensor_max_y: int = dataclasses.field(init=False, repr=False)

    def _get_boundary(self, diff_fn: Callable[[int, int], int], axis: str) -> int:
        return diff_fn(getattr(self.sensor, axis), self.distance)

    def __post_init__(self) -> None:
        self.distance = self.sensor.distance(self.beacon)
        self.sensor_min_x = self._get_boundary(operator.sub, "x")
        self.sensor_max_x = self._get_boundary(operator.add, "x")
        self.sensor_min_y = self._get_boundary(operator.sub, "y")
        self.sensor_max_y = self._get_boundary(operator.add, "y")


def parse_reading_input(reading_input: str) -> list[Reading]:
    readings = []
    for raw_reading in reading_input.splitlines():
        result = parse.parse(
            "Sensor at x={sensor[x]:d}, y={sensor[y]:d}: closest beacon is at x={beacon[x]:d}, y={beacon[y]:d}",
            raw_reading,
        )
        readings.append(
            Reading(
                sensor=Coords(**result["sensor"]),
                beacon=Coords(**result["beacon"]),
            )
        )
    return readings


def merge_overlapping_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals = sorted(intervals)
    left, right = intervals[:1], intervals[1:]
    for next_i in right:
        last_i = left.pop()
        if last_i[0] <= next_i[0] <= last_i[1]:
            i = [last_i[0], max(last_i[1], next_i[1])]
            left.append(i)
        else:
            left.extend([last_i, next_i])
    return left


def _get_sensor_x_range(reading: Reading, y_axis: int) -> list[int] | None:
    if not reading.sensor_min_y <= y_axis <= reading.sensor_max_y:
        return None
    y_offset = abs(reading.sensor.y - y_axis)
    x_range = [reading.sensor_min_x + y_offset, reading.sensor_max_x - y_offset]
    return x_range


def _get_sensor_x_ranges(readings: list[Reading], y_axis: int) -> list[list[int]]:
    x_ranges = []
    for reading in readings:
        x_range = _get_sensor_x_range(reading, y_axis)
        if x_range is None:
            continue
        x_ranges.append(x_range)
    merged_x_ranges = merge_overlapping_intervals(x_ranges)
    return merged_x_ranges


def sum_positions_without_beacon(readings: list[Reading], y_axis: int) -> int:
    beacon_xs_on_y_axis = {
        reading.beacon.x for reading in readings if reading.beacon.y == y_axis
    }
    positions_with_beacons = 0
    known_beacons = 0
    for range_start, range_end in _get_sensor_x_ranges(readings, y_axis):
        for x in beacon_xs_on_y_axis:
            if range_start <= x <= range_end:
                known_beacons += 1
                break
        positions_with_beacons += range_end - range_start + 1
    return positions_with_beacons - known_beacons


def _do_missing_beacon_search_for_row(
    sensor_ranges: list[list[int]], start_x: int, end_x: int
) -> int | None:

    beacon_surrounding_ranges = []
    sensor_range_it = iter(sensor_ranges)
    for range in sensor_range_it:
        start_x_in_range = range[0] <= start_x <= range[1]
        if not start_x_in_range:
            continue

        end_x_in_range = range[0] <= end_x <= range[1]
        if end_x_in_range:
            # start_x and end_x fully within this range so no missing beacon here
            return None

        # missing beacon is nearby! Grab surrounding ranges and leave
        try:
            next_range = next(sensor_range_it)
        except StopIteration as exc:
            raise ValueError("Unexpected outcome") from exc
        beacon_surrounding_ranges.extend([range, next_range])
        break

    if len(beacon_surrounding_ranges) != 2:
        raise ValueError("Unexpected outcome")
    left_range, right_range = beacon_surrounding_ranges
    assert (right_range[0] - left_range[1]) == 2
    return left_range[1] + 1


def missing_beacon_search(readings: list[Reading], start: int, end: int) -> Coords:
    for y in range(start, end):
        sensor_ranges = _get_sensor_x_ranges(readings, y)
        x = _do_missing_beacon_search_for_row(sensor_ranges, start, end)
        if x is not None:
            return Coords(x, y)
    raise ValueError("We didn't find the missing beacon")


def missing_beacon_tuning_freq(readings: list[Reading], start: int, end: int) -> int:
    beacon = missing_beacon_search(readings, start, end)
    return 4_000_000 * beacon.x + beacon.y


def main() -> None:
    reading_input = read_file()
    readings = parse_reading_input(reading_input)

    y_axis = 2_000_000
    print(
        f"Number of positions with no beacon in y={y_axis}:",
        sum_positions_without_beacon(readings, y_axis),
    )

    print(
        f"Missing beacon tuning frequency:",
        missing_beacon_tuning_freq(readings, start=0, end=4_000_000),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
