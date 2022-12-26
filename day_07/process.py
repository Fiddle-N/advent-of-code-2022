import dataclasses
import operator
from collections.abc import Callable
from typing import Optional, Union

import more_itertools


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


@dataclasses.dataclass
class Dir:
    files: dict[str, Union[int, "Dir"]]
    parent: Optional["Dir"] = dataclasses.field(
        compare=False
    )  # ignore parent reference for __eq__ checks to avoid RecursionError

    @property
    def size(self) -> int:
        return sum(
            (file.size if isinstance(file, Dir) else file)
            for file in self.files.values()
        )


def process_out(out: str) -> Dir:
    lines = out.splitlines()
    sections = more_itertools.split_before(lines, lambda line: line[0] == "$")

    dir_ = None
    curr_dir = None
    for section in sections:
        match section:
            case [cd]:
                match cd.split():
                    case ["$", "cd", "/"]:
                        assert dir_ is None
                        dir_ = Dir(
                            files={},
                            parent=None,
                        )
                        curr_dir = dir_
                    case ["$", "cd", ".."]:
                        assert curr_dir
                        curr_dir = curr_dir.parent
                    case ["$", "cd", dir_name]:
                        assert curr_dir
                        next_dir = curr_dir.files[dir_name]
                        assert isinstance(next_dir, Dir)
                        curr_dir = next_dir
                    case _:
                        raise ValueError("Unexpected command")
            case ["$ ls", *files]:
                for file in files:
                    match file.split():
                        case ["dir", dir_name]:
                            assert curr_dir
                            curr_dir.files[dir_name] = Dir(
                                files={},
                                parent=curr_dir,
                            )
                        case [size, file_name]:
                            assert curr_dir
                            curr_dir.files[file_name] = int(size)
                        case _:
                            raise ValueError("Unexpected command")
            case _:
                raise ValueError("Unexpected command")

    assert dir_
    return dir_


def _dir_search(fs: Dir, size: int, comp_fn: Callable[[int, int], bool]) -> list[Dir]:
    dirs = []

    def search(dir_: Dir) -> None:
        if comp_fn(dir_.size, size):
            dirs.append(dir_)
        for file in dir_.files.values():
            if isinstance(file, Dir):
                search(file)

    search(fs)
    return dirs


def dirs_below_100k(fs: Dir) -> list[Dir]:
    return _dir_search(fs, size=100_000, comp_fn=operator.le)


def dirs_to_free_space(fs: Dir) -> list[Dir]:
    size_left = 70_000_000 - fs.size
    size_req = 30_000_000 - size_left

    return _dir_search(fs, size=size_req, comp_fn=operator.ge)


def sum_dirs_below_100k(fs: Dir) -> int:
    dirs_ = dirs_below_100k(fs)
    return sum(dir_.size for dir_ in dirs_)


def min_dir_size_to_free_space(fs: Dir) -> int:
    dirs_ = dirs_to_free_space(fs)
    return min(dir_.size for dir_ in dirs_)


def main() -> None:
    out = read_file()
    fs = process_out(out)

    print("Sum of all directories with size at most 100k:", sum_dirs_below_100k(fs))
    print(
        "Size of smallest directory that, if deleted, would free up space to run update:",
        min_dir_size_to_free_space(fs),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
