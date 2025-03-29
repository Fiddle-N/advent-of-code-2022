# BROKEN TODO remove before you count
import dataclasses
from typing import Optional


def sign_magnitude_mod(num: int, mod: int):
    # to reduce the number of times to go around the list
    result = num % mod
    if num < 0 and result > 0:
        result = result - mod
    return result


@dataclasses.dataclass
class Node:
    data: int
    prev: Optional['Node'] = None
    next: Optional['Node'] = None

    def __repr__(self):
        return f"<Node data={self.data} prev={self.prev.data} next={self.next.data}>"


class DoublyLinkedList:

    def __init__(self):
        self.first = None
        self._len = 0

    def insert_after(self, ref_node: Node, new_node: Node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node
        self._len += 1

    def insert_before(self, ref_node: Node, new_node: Node):
        self.insert_after(ref_node.prev, new_node)

    def append(self, new_node: Node):
        if self.first is None:
            self.first = new_node
            new_node.prev = new_node
            new_node.next = new_node
            self._len += 1
        else:
            self.insert_after(self.first.prev, new_node)

    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next
        self._len -= 1

    def __len__(self):
        return self._len


class GrovePositioningSystem:

    def __init__(self, grove_data):
        self.grove_data = [int(num) for num in grove_data.splitlines()]

        self.grove_nodes = []
        for num in self.grove_data:
            node = Node(data=num)
            self.grove_nodes.append(node)
            if num == 0:
                self.node_zero = node

        self.grove_linked_list = DoublyLinkedList()
        for node in self.grove_nodes:
            self.grove_linked_list.append(node)

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read())

    def __iter__(self):
        for node in self.grove_nodes:

            if node.data == 0:
                pass
            elif node.data < 0:
                moves = sign_magnitude_mod(node.data, len(self.grove_linked_list))
                assert moves <= 0
                if moves != 0:
                    target_node = node
                    for _ in range(-moves):
                        target_node = target_node.prev

                    self.grove_linked_list.remove(node)
                    self.grove_linked_list.insert_before(target_node, node)
            elif node.data > 0:
                moves = sign_magnitude_mod(node.data, len(self.grove_linked_list))
                assert moves >= 0
                if moves != 0:
                    target_node = node
                    for _ in range(moves):
                        target_node = target_node.next

                    self.grove_linked_list.remove(node)
                    self.grove_linked_list.insert_after(target_node, node)


            # if node.data == 0:
            #     pass
            # elif node.data < 0:
            #     target_node = node
            #     for _ in range(-node.data):
            #         target_node = target_node.prev
            #
            #     if node != target_node:
            #         self.grove_linked_list.remove(node)
            #         self.grove_linked_list.insert_before(target_node, node)
            # elif node.data > 0:
            #     target_node = node
            #     for _ in range(node.data):
            #         target_node = target_node.next
            #
            #     if node != target_node:
            #         self.grove_linked_list.remove(node)
            #         self.grove_linked_list.insert_after(target_node, node)

            # moves = node.data
            # moves = moves % len(self.grove_linked_list)
            # if node.data < 0:
            #     moves -= 1
            # if moves != 0:
            #     target_node = node
            #     for _ in range(moves):
            #         target_node = target_node.next
            #
            #     self.grove_linked_list.remove(node)
            #     self.grove_linked_list.insert_after(target_node, node)
            # else:
            #     print(moves)
            #     print('why')
            #     print()

            yield


    def get_key_nos(self):
        values = []

        thousand_moves = 1000 % len(self.grove_linked_list)

        target_node = self.node_zero

        for _ in range(3):
            for __ in range(thousand_moves):
                target_node = target_node.next
            values.append(target_node.data)

        return sum(values)


def main() -> None:
    gps = GrovePositioningSystem.read_file()

    gps_it = iter(gps)

    for _ in gps_it:
        pass

    print("Sum of three numbers that form grove coordinates:", gps.get_key_nos())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
