import pytest

from day_03 import process


@pytest.mark.parametrize(
    "rucksacks, sum_priorities",
    [
        ('vJrwpWtwJgWrhcsFMMfFFhFp', 16),
        ('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL', 38),
        ('PmmdzqPrVvPwwTWBwg', 42),
        ('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn', 22),
        ('ttgJtRGJQctTZtZT', 20),
        ('CrZsJsPPZsGzwwsLwLmpwMDw', 19),
        (
                """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""", 157
        )
    ]
)
def test_rucksack_reorganisation_sum_priorities_of_common_items_across_rucksack_compartments(rucksacks: str, sum_priorities: int) -> None:
    contents = f"""\
{rucksacks}
"""
    rr = process.RucksackReorganisation(contents)
    assert rr.sum_priorities_of_common_items_across_rucksack_compartments() == sum_priorities


@pytest.mark.parametrize(
    "rucksacks, sum_priorities",
    [
        (
                """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg""", 18
        ),
        (
                """\
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""", 52
        ),
        (
                """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""", 70
        ),
    ]
)
def test_rucksack_reorganisation_sum_priorities_of_common_items_across_elf_group_rucksacks(rucksacks: str, sum_priorities: int) -> None:
    contents = f"""\
{rucksacks}
"""
    rr = process.RucksackReorganisation(contents)
    assert rr.sum_priorities_of_common_items_across_elf_group_rucksacks() == sum_priorities
