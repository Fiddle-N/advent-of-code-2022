from typing import Callable


class ElfRange(set[int]):
    def __init__(self, start: int, end: int):
        assert end >= start
        self.start = start
        self.end = end
        super().__init__(range(start, end + 1))

    def __repr__(self) -> str:
        return f"ElfRange({self.start}, {self.end})"

    def contains(self, item: "ElfRange") -> bool:
        return self >= item

    def overlaps(self, item: "ElfRange") -> bool:
        return bool(self & item)


class CampCleanup:
    def __init__(self, section_assignment_input: str) -> None:
        self.section_pairs = [
            tuple(
                ElfRange(*[int(boundary) for boundary in section.split("-")])
                for section in section_assignment_pair.split(",")
            )
            for section_assignment_pair in section_assignment_input.splitlines()
        ]

    @classmethod
    def read_file(cls) -> "CampCleanup":
        with open("input.txt") as f:
            return cls(f.read())

    @staticmethod
    def _two_way_contains(range1: ElfRange, range2: ElfRange) -> bool:
        return range1.contains(range2) or range2.contains(range1)

    def _sum_comp(self, comp_fn: Callable[[ElfRange, ElfRange], bool]) -> int:
        return sum(comp_fn(*pair) for pair in self.section_pairs)

    def sum_ranges_containing_other_ranges(self) -> int:
        return self._sum_comp(self._two_way_contains)

    def sum_ranges_overlapping_other_ranges(self) -> int:
        return self._sum_comp(ElfRange.overlaps)


def main() -> None:
    cc = CampCleanup.read_file()
    print(
        "Ranges fully containing other ranges:",
        cc.sum_ranges_containing_other_ranges(),
    )
    print(
        "Ranges overlapping other ranges:",
        cc.sum_ranges_overlapping_other_ranges(),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
