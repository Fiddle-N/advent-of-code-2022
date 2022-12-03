import dataclasses
import string

import more_itertools


PRIORITIES = [None] + list(string.ascii_letters)


@dataclasses.dataclass(frozen=True)
class Rucksack:
    contents: str

    @property
    def compartments(self) -> list[str]:
        assert len(self.contents) % 2 == 0  # verify even number of items in rucksack
        return [
            ''.join(compartment)
            for compartment in more_itertools.divide(2, self.contents)
        ]


class Rucksacks(list):

    def __repr__(self):
        return f"Rucksacks[{super().__repr__()}]"

    @property
    def elf_groups(self):
        assert len(self) % 3 == 0  # verify rucksacks can be split amongst each group of three elves
        return list(more_itertools.chunked(self, n=3))


class RucksackReorganisation:

    def __init__(self, contents):
        self.rucksacks = Rucksacks([Rucksack(rucksack_contents) for rucksack_contents in contents.splitlines()])

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    @staticmethod
    def _get_sum_priorities(contents_groups: list[list[str]]):
        sum_priorities = 0
        for contents_group in contents_groups:
            common_items = set.intersection(
                *[set(contents) for contents in contents_group]
            )
            try:
                common_item, = common_items
            except ValueError as exc:
                raise ValueError('More than one common item retrieved') from exc
            sum_priorities += PRIORITIES.index(common_item)
        return sum_priorities

    def sum_priorities_of_common_items_across_rucksack_compartments(self):
        rucksack_compartments = [rucksack.compartments for rucksack in self.rucksacks]
        return self._get_sum_priorities(rucksack_compartments)

    def sum_priorities_of_common_items_across_elf_group_rucksacks(self):
        elf_group_rucksacks = [
            [rucksack.contents for rucksack in rucksack_group]
            for rucksack_group in self.rucksacks.elf_groups
        ]
        return self._get_sum_priorities(elf_group_rucksacks)


def main():
    rr = RucksackReorganisation.read_file()
    print(
        'Sum priorities of common items in compartments within each rucksack:',
        rr.sum_priorities_of_common_items_across_rucksack_compartments(),
    )
    print(
        'Sum priorities of common items across rucksacks in each elf group:',
        rr.sum_priorities_of_common_items_across_elf_group_rucksacks(),
    )


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
