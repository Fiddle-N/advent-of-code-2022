from day_01 import process


def test_calories_of_elf_carrying_most_calories():
    inventory_input = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    cc = process.CalorieCounting(inventory_input)
    assert cc.calculate_calories_of_elf_carrying_most_calories() == 24_000


def test_calories_of_top_three_elves_carrying_most_calories():
    inventory_input = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
    cc = process.CalorieCounting(inventory_input)
    assert cc.calculate_calories_of_top_three_elves_carrying_most_calories() == 45_000
