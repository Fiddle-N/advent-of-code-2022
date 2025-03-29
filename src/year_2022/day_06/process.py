import functools
from typing import Optional

import more_itertools


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


def _detect_marker_idx(datastream: str, n: int) -> Optional[int]:
    for idx, putative_marker in enumerate(
        more_itertools.windowed(datastream, n), start=n
    ):
        if len(set(putative_marker)) == n:
            return idx
    return None


detect_start_of_packet_marker_idx = functools.partial(_detect_marker_idx, n=4)

detect_start_of_message_marker_idx = functools.partial(_detect_marker_idx, n=14)


def main() -> None:
    file_txt = read_file()

    print("Start-of-packet marker index:", detect_start_of_packet_marker_idx(file_txt))
    print(
        "Start-of-message marker index:", detect_start_of_message_marker_idx(file_txt)
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
