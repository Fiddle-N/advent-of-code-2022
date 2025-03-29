import collections
import dataclasses


@dataclasses.dataclass(eq=False)
class Node:
    number: int

    def __repr__(self):
        return repr(self.number)


class GrovePositioningSystem:

    def __init__(self, grove_data, apply_decryption_key=False, mix_number=1):
        decryption_key = 811589153 if apply_decryption_key else 1
        self.grove_data = [int(num) * decryption_key for num in grove_data.splitlines()]

        self.grove_nodes = []
        for num in self.grove_data:
            node = Node(num)
            self.grove_nodes.append(node)
            if num == 0:
                self.node_zero = node

        self.grove_linked_list = collections.deque()
        for node in self.grove_nodes:
            self.grove_linked_list.append(node)
        self.mix_number = mix_number

    @classmethod
    def read_file(cls, apply_decryption_key=False, mix_number=1):
        with open("input.txt") as f:
            return cls(f.read(), apply_decryption_key, mix_number)

    def locate(self, node):
        while True:
            if node == self.grove_linked_list[0]:
                return
            self.grove_linked_list.rotate()

    def __iter__(self):
        for _ in range(self.mix_number):
            for node in self.grove_nodes:
                self.locate(node)
                node_again = self.grove_linked_list.popleft()
                assert node == node_again
                rotate_no = node.number % len(self.grove_linked_list)
                self.grove_linked_list.rotate(-rotate_no)
                self.grove_linked_list.appendleft(node)
                yield

    def get_key_nos(self):
        values = []

        self.locate(self.node_zero)

        for _ in range(3):
            self.grove_linked_list.rotate(-1000)
            values.append(self.grove_linked_list[0].number)

        return sum(values)


def main() -> None:
    gps = GrovePositioningSystem.read_file()
    gps_it = iter(gps)
    for _ in gps_it:
        pass
    print("Sum of three numbers that form grove coordinates without decryption key for one mix:", gps.get_key_nos())

    gps_2 = GrovePositioningSystem.read_file(apply_decryption_key=True, mix_number=10)
    gps_it_2 = iter(gps_2)
    for _ in gps_it_2:
        pass
    print("Sum of three numbers that form grove coordinates with decryption key for 10 mixes:", gps_2.get_key_nos())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
