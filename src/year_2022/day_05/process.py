import dataclasses
from typing import Optional, Literal, Iterator

import parse  # type: ignore


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


class CrateStacks(list[Optional[list[str]]]):
    @classmethod
    def from_text(cls, stack_txt: str) -> "CrateStacks":
        stack_list = reversed(stack_txt.splitlines())
        header, stack_contents = next(stack_list), list(stack_list)
        assert (
            max(int(crate_no) for crate_no in header.strip().split()) <= 9
        )  # Only a single-digit number of stacks are supported
        stack_text_indices = [
            (int(ele), idx) for idx, ele in enumerate(header) if ele != " "
        ]
        stacks: list[Optional[list[str]]] = [None] + [[] for _ in stack_text_indices]

        for row in stack_contents:
            for stack_index, stack_text_index in stack_text_indices:
                stack_value = row[stack_text_index]
                if stack_value != " ":  # found a stack value
                    stack = stacks[stack_index]
                    assert stack is not None
                    stack.append(stack_value)
        return cls(stacks)

    @property
    def end_crates(self) -> str:
        return "".join(stack[-1] for stack in self if stack is not None)


@dataclasses.dataclass
class Rearrangement:
    moves: int
    start: int
    end: int

    @classmethod
    def from_text(cls, rearrangement_txt: str) -> "Rearrangement":
        parsed_text = parse.parse(
            "move {move:d} from {start:d} to {end:d}", rearrangement_txt
        )
        return cls(parsed_text["move"], parsed_text["start"], parsed_text["end"])


class SupplyStacks:
    def __init__(self, input_txt: str, crane_type: Literal["9000", "9001"]) -> None:
        stacks_txt, rearrangements_txt = input_txt.split("\n\n")
        self.crate_stacks = CrateStacks.from_text(stacks_txt)
        self.rearrangement_proc = [
            Rearrangement.from_text(rearrangement_txt)
            for rearrangement_txt in rearrangements_txt.splitlines()
        ]
        self.crane_type = crane_type

    def _rearrange(self, rearrangement: Rearrangement) -> CrateStacks:
        start_stack = self.crate_stacks[rearrangement.start]
        end_stack = self.crate_stacks[rearrangement.end]
        assert start_stack is not None
        assert end_stack is not None
        picked_up = []
        for _ in range(rearrangement.moves):
            picked_up.append(start_stack.pop())
        if self.crane_type == "9000":
            dropped_off = picked_up
        elif self.crane_type == "9001":
            dropped_off = list(reversed(picked_up))
        else:
            raise Exception("Unexpected crane mode")
        end_stack.extend(dropped_off)
        return self.crate_stacks

    def __iter__(self) -> Iterator[CrateStacks]:
        for rearrangement in self.rearrangement_proc:
            yield self._rearrange(rearrangement)


def run_crane(file_txt: str, crane_type: Literal["9000", "9001"]) -> None:
    ss = SupplyStacks(file_txt, crane_type=crane_type)
    for _ in iter(ss):
        pass
    print(
        f"End crates after rearrangement procedure with CraneMover {crane_type}:",
        ss.crate_stacks.end_crates,
    )


def main() -> None:
    file_txt = read_file()

    run_crane(file_txt, "9000")
    run_crane(file_txt, "9001")


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
