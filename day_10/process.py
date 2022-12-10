import collections
from collections.abc import Iterator, Container
import dataclasses
import enum
import itertools


class CycleState(enum.Enum):
    START = enum.auto()
    DURING = enum.auto()
    AFTER = enum.auto()


@dataclasses.dataclass(frozen=True)
class Cycle:
    no: int
    state: CycleState


@dataclasses.dataclass
class Instr:
    cycle_no: int
    add_val: int

    def decrement_cycle(self) -> None:
        self.cycle_no -= 1


class CathodeRayTube:
    def __init__(self, program: str, watch_cycles: Container[Cycle] = ()) -> None:
        self.program = collections.deque(program.splitlines())

        self.register = 1

        self._cycle_gen = self._cycle_gen_fn()
        self.cycle: Cycle

        self.instr: Instr | None = None

        self._watch_cycles = watch_cycles
        self.watched_cycles: dict[Cycle, int] = {}

        self.screen = ""

    @classmethod
    def read_file(cls, watch_cycles: Container[Cycle] = ()) -> "CathodeRayTube":
        with open("input.txt") as f:
            return cls(f.read(), watch_cycles=watch_cycles)

    @staticmethod
    def _cycle_gen_fn() -> Iterator[Cycle]:
        for x in itertools.count(1):
            for y in CycleState:
                yield Cycle(x, y)

    def _increment_cycle(self) -> None:
        self.cycle = next(self._cycle_gen)

    def _parse_instr(self, instr_text: str) -> None:
        match instr_text.split():
            case ["noop"]:
                instr = Instr(cycle_no=1, add_val=0)
            case ["addx", add_val]:
                instr = Instr(cycle_no=2, add_val=int(add_val))
            case _:
                raise Exception("Unexpected instruction")
        self.instr = instr

    def _execute_pre_cycle(self) -> None:
        if self.instr is None:
            try:
                instr_txt = self.program.popleft()
            except IndexError as exc:
                raise StopIteration from exc
            self._parse_instr(instr_txt)

    def _execute_mid_cycle(self) -> None:
        if ((self.cycle.no - 1) % 40) in (
            self.register - 1,
            self.register,
            self.register + 1,
        ):
            self.screen += "#"
        else:
            self.screen += "."

        if self.cycle.no % 40 == 0:
            self.screen += "\n"

    def _execute_post_cycle(self) -> None:
        assert self.instr
        self.instr.decrement_cycle()
        if self.instr.cycle_no == 0:
            self.register += self.instr.add_val
            self.instr = None

    @property
    def signal_strength(self) -> int:
        return self.cycle.no * self.register

    def __iter__(self) -> "CathodeRayTube":
        return self

    def __next__(self) -> int:
        self._increment_cycle()

        cycle_fns = {
            CycleState.START: self._execute_pre_cycle,
            CycleState.DURING: self._execute_mid_cycle,
            CycleState.AFTER: self._execute_post_cycle,
        }

        cycle_fns[self.cycle.state]()

        if self.cycle in self._watch_cycles:
            self.watched_cycles[self.cycle] = self.signal_strength

        return self.signal_strength


def main() -> None:
    key_cycles = [
        Cycle(no=20, state=CycleState.DURING),
        Cycle(no=60, state=CycleState.DURING),
        Cycle(no=100, state=CycleState.DURING),
        Cycle(no=140, state=CycleState.DURING),
        Cycle(no=180, state=CycleState.DURING),
        Cycle(no=220, state=CycleState.DURING),
    ]

    crt = CathodeRayTube.read_file(watch_cycles=key_cycles)

    for _ in crt:
        pass

    print(
        "Sum of interesting signal strengths:",
        sum(crt.watched_cycles.values()),
        end="\n\n",
    )
    print("Screen:\n")
    print(crt.screen)


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
