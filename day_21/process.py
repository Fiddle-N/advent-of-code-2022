import collections
import dataclasses
import itertools
import operator
from typing import Callable

import parse


class HumanError(ValueError):
    """Raise when we encounter humn in our monkey maths dependency chain"""


def intdiv(x, y):
    assert x % y == 0
    return operator.floordiv(x, y)


OP_FNS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": intdiv,
}

OPP_FNS = {
    operator.add: operator.sub,
    operator.sub: operator.add,
    operator.mul: intdiv,
    intdiv: operator.mul,
}


@dataclasses.dataclass
class Operation:
    name: str
    operands: tuple[str, str]
    op_fn: Callable[[int, int], int]


class MonkeyMath:
    def __init__(self, riddle):
        self.operations = {}
        self.numbers = {}
        for line in riddle.splitlines():
            name, expr = self._process_line(line)
            match expr:
                case Operation():
                    self.operations[name] = expr
                case int():
                    self.numbers[name] = expr
                case _:
                    raise ValueError("Unexpected line")
        self.root = "root"
        self.human = "humn"
        # self.numbers['humn'] = 2655454

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read())

    def _process_line(self, line) -> tuple[str, Operation | int]:
        if match := parse.parse(
            "{name}: {left_operand} {operation} {right_operand}", line
        ):
            return match["name"], Operation(
                name=match["name"],
                operands=(match["left_operand"], match["right_operand"]),
                op_fn=OP_FNS[match["operation"]],
            )
        elif match := parse.parse("{name}: {number:d}", line):
            return match["name"], match["number"]
        else:
            raise ValueError("Unexpected line")

    def _calculate(self, name, operations, numbers, raise_exc_for=""):
        stack = collections.deque([name])
        numbers = numbers.copy()
        while stack:
            op_name = stack.popleft()
            if op_name in numbers:
                # we've processed this operation before
                continue
            op = operations[op_name]

            if any((operand == raise_exc_for) for operand in op.operands):
                raise HumanError

            if all(operand in numbers for operand in op.operands):
                numbers[op.name] = op.op_fn(
                    *[numbers[operand] for operand in op.operands]
                )
            else:
                stack.extendleft([op_name, op.operands[0], op.operands[1]])
        try:
            result = numbers[name]
        except KeyError as exc:
            raise RuntimeError("Monkey math calculation failed") from exc
        return result

    def calculate_root(self):
        return self._calculate(
            name=self.root, operations=self.operations, numbers=self.numbers
        )

    def _check_for_humn(self, name):
        try:
            self._calculate(
                name,
                operations=self.operations,
                numbers=self.numbers,
                raise_exc_for=self.human,
            )
        except HumanError:
            return True
        else:
            return False

    def _invert(self, op, operations):
        new_ops = []
        left_operand, right_operand = op.operands
        if left_operand in operations or left_operand == self.human:
            new_ops.append(
                Operation(
                    name=left_operand,
                    operands=(op.name, right_operand),
                    op_fn=OPP_FNS[op.op_fn],
                )
            )
        if right_operand in operations or right_operand == self.human:
            if op.op_fn in (operator.add, operator.mul):
                new_op = Operation(
                    name=right_operand,
                    operands=(op.name, left_operand),
                    op_fn=OPP_FNS[op.op_fn],
                )
            elif op.op_fn in (operator.sub, intdiv):
                new_op = Operation(
                    name=right_operand,
                    operands=(left_operand, op.name),
                    op_fn=op.op_fn,
                )
            else:
                raise Exception
            new_ops.append(new_op)
        return new_ops

    def _invert_for_humn(self, name, operations, numbers):
        new_ops = {}
        new_nums = {}
        stack = collections.deque([name])
        while stack:
            op_name = stack.popleft()

            if op_name == self.human:
                continue

            if op_name in numbers:
                new_nums[op_name] = numbers[op_name]
                continue

            op = operations[op_name]
            invert_ops = self._invert(op, operations)
            if len(invert_ops) == 2:

                print('here')
            for invert_op in invert_ops:
                new_ops[invert_op.name] = invert_op
            stack.extendleft(op.operands)
        return new_ops, new_nums

    def _find_paths(self, name, target_name, operations):
        operations = operations.copy()
        stack = collections.deque([name])
        paths = collections.defaultdict(list)
        while stack:
            op_name = stack.popleft()
            if op_name in paths:
                continue
            op = operations[op_name]
            not_found_operands = []
            none_operands = []
            for operand in op.operands:
                if operand in paths:
                    for path in paths[operand]:
                        paths[op_name].append((op_name,) + path)
                elif operand not in operations:
                    if operand == target_name:
                        paths[op_name].append((op_name, operand))
                    else:
                        none_operands.append(None)
                elif operand in operations:
                    not_found_operands.append(operand)
            if not_found_operands:
                stack.extendleft([op_name, *not_found_operands])
            if none_operands == [None, None]:
                operations.pop(op_name)
        try:
            result = paths[name]
        except KeyError as exc:
            raise RuntimeError("Monkey math calculation failed") from exc
        return result

    def _invert_2(self, name, operand, operations):
        op = operations[name]

        left_operand, right_operand = op.operands
        if operand == left_operand:
            new_op = Operation(
                name=left_operand,
                operands=(op.name, right_operand),
                op_fn=OPP_FNS[op.op_fn],
            )
        elif operand == right_operand:
            if op.op_fn in (operator.add, operator.mul):
                new_op = Operation(
                    name=right_operand,
                    operands=(op.name, left_operand),
                    op_fn=OPP_FNS[op.op_fn],
                )
            elif op.op_fn in (operator.sub, intdiv):
                new_op = Operation(
                    name=right_operand,
                    operands=(left_operand, op.name),
                    op_fn=op.op_fn,
                )
            else:
                raise Exception
        else:
            raise Exception
        return new_op

    def _invert_for_humn_2(self, path, operations):
        invert_ops = {}
        for name, operand in reversed(list(itertools.pairwise(path))):
            invert_op = self._invert_2(name, operand, operations)
            invert_ops[invert_op.name] = invert_op

        new_ops = operations | invert_ops
        new_ops.pop(path[0])
        return new_ops

    def calculate_root_equality_test(self):
        root_operands = self.operations[self.root].operands

        operations = self.operations.copy()
        operations.pop(
            self.root
        )  # remove root as it no longer makes sense in the collection (not strictly necessary though)

        human_check = {
            operand: self._check_for_humn(operand) for operand in root_operands
        }
        assert (len(human_check) == 2) and (
            set(human_check.values())
            == {
                True,
                False,
            }
        )  # humn can only be on one side of the equation for it to be solvable as a linear equation
        operand_with_humn = [
            operand for operand, check in human_check.items() if check
        ][0]
        operand_without_humn = [
            operand for operand, check in human_check.items() if not check
        ][0]

        target = self._calculate(
            name=operand_without_humn, operations=operations, numbers=self.numbers
        )

        paths = self._find_paths(name=operand_with_humn, target_name=self.human, operations=operations)
        assert len(paths) == 1
        path, = paths

        invert_ops = self._invert_for_humn_2(path, operations)

        invert_nums = self.numbers.copy()
        invert_nums[operand_with_humn] = target
        invert_nums.pop(self.human)


        result = self._calculate(
            name=self.human, operations=invert_ops, numbers=invert_nums
        )

        return result


def main() -> None:
    mm = MonkeyMath.read_file()

    print("Root number:", mm.calculate_root())
    print("Number to pass root equality test:", mm.calculate_root_equality_test())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
