import pytest

from day_04 import process


@pytest.mark.parametrize(
    "elf1_range_vals, elf2_range_vals, is_contained_in, contains",
    [
        ((2, 4), (6, 8), False, False),
        ((2, 3), (4, 5), False, False),
        ((5, 7), (7, 9), False, False),
        ((2, 8), (3, 7), False, True),
        ((6, 6), (4, 6), True, False),
        ((2, 6), (4, 8), False, False),
    ],
)
def test_elf_range_contains(
    elf1_range_vals: tuple[int, int],
    elf2_range_vals: tuple[int, int],
    is_contained_in: bool,
    contains: bool,
) -> None:
    elf0_range = process.ElfRange(elf1_range_vals[0], elf1_range_vals[1])
    elf1_range = process.ElfRange(elf2_range_vals[0], elf2_range_vals[1])

    assert elf1_range.contains(elf0_range) == is_contained_in
    assert elf0_range.contains(elf1_range) == contains


def test_camp_cleanup_ranges_containing_other_ranges() -> None:
    section_assignment_input = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    cc = process.CampCleanup(section_assignment_input)
    assert cc.sum_ranges_containing_other_ranges() == 2


@pytest.mark.parametrize(
    "elf1_range_vals, elf2_range_vals, overlaps",
    [
        ((2, 4), (6, 8), False),
        ((2, 3), (4, 5), False),
        ((5, 7), (7, 9), True),
        ((2, 8), (3, 7), True),
        ((6, 6), (4, 6), True),
        ((2, 6), (4, 8), True),
    ],
)
def test_elf_range_overlaps(
    elf1_range_vals: tuple[int, int],
    elf2_range_vals: tuple[int, int],
    overlaps: bool,
) -> None:
    elf0_range = process.ElfRange(elf1_range_vals[0], elf1_range_vals[1])
    elf1_range = process.ElfRange(elf2_range_vals[0], elf2_range_vals[1])

    assert elf0_range.overlaps(elf1_range) == overlaps


def test_camp_cleanup_ranges_overlapping_other_ranges() -> None:
    section_assignment_input = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
    cc = process.CampCleanup(section_assignment_input)
    assert cc.sum_ranges_overlapping_other_ranges() == 4
