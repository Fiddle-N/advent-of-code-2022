
class CalorieCounting:

    def __init__(self, inventory_input: str):
        raw_inventory = [
            [int(item) for item in elf_items.split('\n')]
            for elf_items in inventory_input.strip().split('\n\n')
        ]
        self._inventory = sorted([sum(elf_inventory) for elf_inventory in raw_inventory], reverse=True)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    @property
    def calories_of_elf_carrying_most_calories(self):
        return self._inventory[0]

    @property
    def calories_of_top_three_elves_carrying_most_calories(self):
        return sum(self._inventory[:3])


def main():
    cc = CalorieCounting.read_file()
    print('Total calories of elf carrying most calories:', cc.calories_of_elf_carrying_most_calories)
    print('Total calories of top 3 elves carrying most calories:', cc.calories_of_top_three_elves_carrying_most_calories)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))
