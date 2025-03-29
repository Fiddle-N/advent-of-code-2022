import collections
import dataclasses
import functools
import math
import operator
from typing import Callable, Iterable, NoReturn, Any, Iterator

import parse  # type: ignore


OP_FNS = {
    "+": operator.add,
    "*": operator.mul,
}


class MonkeyItems(collections.deque[int]):
    def __init__(self, iterable: Iterable[int] = (), maxlen: int | None = None) -> None:
        self.inspects = 0
        super().__init__(iterable, maxlen)

    def popleft(self) -> int:
        self.inspects += 1
        return super().popleft()


@dataclasses.dataclass
class Monkey:
    items: MonkeyItems
    op: Callable[[int], int]
    div_test: int
    if_true: int
    if_false: int

    @property
    def insp_no(self) -> int:
        return self.items.inspects


class Monkeys(list[Monkey]):
    def __str__(self) -> str:
        return "\n".join(
            f"Monkey {monkey_no}: {', '.join([str(item) for item in monkey.items])}"
            for monkey_no, monkey in enumerate(self)
        )

    def insp_summary(self) -> str:
        return "\n".join(
            f"Monkey {monkey_no} inspected items {monkey.insp_no} times."
            for monkey_no, monkey in enumerate(self)
        )

    @property
    def insp_nos(self) -> list[int]:
        return [monkey.insp_no for monkey in self]

    @property
    def biz(self) -> int:
        sorted_insps = sorted(self.insp_nos, reverse=True)
        return sorted_insps[0] * sorted_insps[1]


def raise_unexpected_note_error() -> NoReturn:
    raise ValueError("Unexpected note")


def op_fn_gen(op: str) -> Callable[[int], int]:
    match op.split():
        case ["new", "=", "old", "*", "old"]:
            square_fn = functools.partial(pow, exp=2)
            return square_fn
        case ["new", "=", "old", ("+" | "*") as op, operand]:
            op_fn = functools.partial(OP_FNS[op], int(operand))
            return op_fn
        case _:
            raise_unexpected_note_error()


def parse_notes(notes: str) -> Monkeys:
    monkeys = Monkeys()
    for monkey_note in notes.split("\n\n"):
        monkey_name, *monkey_attrs = monkey_note.splitlines()
        assert "Monkey" in monkey_name

        monkey_dtls: dict[str, Any] = {}
        for attr in monkey_attrs:
            match attr.strip().split(": "):
                case ["Starting items", items]:
                    monkey_dtls["items"] = MonkeyItems(
                        [int(item) for item in items.split(", ")]
                    )
                case ["Operation", op]:
                    monkey_dtls["op"] = op_fn_gen(op)
                case ["Test", div_test]:
                    if parsed := parse.parse("divisible by {div_no:d}", div_test):
                        monkey_dtls["div_test"] = parsed["div_no"]
                    else:
                        raise_unexpected_note_error()
                case ["If true", true_rslt]:
                    if parsed := parse.parse(
                        "throw to monkey {monkey_no:d}", true_rslt
                    ):
                        monkey_dtls["if_true"] = parsed["monkey_no"]
                    else:
                        raise_unexpected_note_error()
                case ["If false", false_rslt]:
                    if parsed := parse.parse(
                        "throw to monkey {monkey_no:d}", false_rslt
                    ):
                        monkey_dtls["if_false"] = parsed["monkey_no"]
                    else:
                        raise_unexpected_note_error()
                case _:
                    raise_unexpected_note_error()
        monkeys.append(Monkey(**monkey_dtls))
    return monkeys


def monkey_insp(monkeys: Monkeys, is_worry_manageable: bool = True) -> Iterator[None]:
    lcm = math.lcm(*[monkey.div_test for monkey in monkeys])
    while True:
        for monkey in monkeys:
            while items := monkey.items:
                lvl = items.popleft()
                if not is_worry_manageable:
                    lvl = lvl % lcm
                insp_lvl = monkey.op(lvl)
                if is_worry_manageable:
                    insp_lvl = insp_lvl // 3
                if insp_lvl % monkey.div_test == 0:
                    monkeys[monkey.if_true].items.append(insp_lvl)
                else:
                    monkeys[monkey.if_false].items.append(insp_lvl)
        yield


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


def main() -> None:
    file_txt = read_file()

    monkeys = parse_notes(file_txt)
    monkey_iter = monkey_insp(monkeys, is_worry_manageable=True)

    no_of_rounds = 20
    for _ in range(no_of_rounds):
        next(monkey_iter)

    print(f"{no_of_rounds} rounds of monkey business:", monkeys.biz)

    monkeys_part_2 = parse_notes(file_txt)
    monkey_iter_2 = monkey_insp(monkeys_part_2, is_worry_manageable=False)

    no_of_rounds = 10_000
    for _ in range(no_of_rounds):
        next(monkey_iter_2)

    print(
        f"{no_of_rounds:,} rounds of monkey business with unmanageable worry:",
        monkeys_part_2.biz,
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
