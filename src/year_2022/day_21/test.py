from day_21 import process


def test_calculate_root():
    riddle = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
    mm = process.MonkeyMath(riddle)
    assert mm.calculate_root() == 152


def test_calculate_root_equality_test():
    riddle = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
    mm = process.MonkeyMath(riddle)
    assert mm.calculate_root_equality_test() == 301


def test_calculate_root_equality_test_multiple_refs_in_one_line():
    # pppw has multiple refs here

    riddle = """\
root: pppw + sjmn
sjmn: 10
pppw: sllz + lgvd
lgvd: ljgn + ptdq
ljgn: 2
ptdq: 3
sllz: humn + dvpt
dvpt: 2
humn: 15
"""
    mm = process.MonkeyMath(riddle)
    assert mm.calculate_root_equality_test() == 3


def test_calculate_root_equality_test_multiple_refs_in_one_line_both_refs_not_leading_to_humn():
    # lgvd has multiple refs here, both its refs do not lead to humn

    riddle = """\
root: pppw + sjmn
sjmn: 10
pppw: lgvd + sllz
lgvd: ljgn + ptdq
ljgn: abcd + efgh
abcd: 1
efgh: 1
ptdq: ijkl + mnop
ijkl: 1
mnop: 2
sllz: humn + dvpt
dvpt: 2
humn: 15
"""
    mm = process.MonkeyMath(riddle)
    assert mm.calculate_root_equality_test() == 3
