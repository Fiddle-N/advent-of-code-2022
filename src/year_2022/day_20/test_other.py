import pytest

from day_20 import process_other


def test():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process_other.GrovePositioningSystem(num_input)

    assert str(gps.grove_linked_list) == 'deque([1, 2, -3, 3, -2, 0, 4])'

    gps_it = iter(gps)

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([1, -3, 3, -2, 0, 4, 2])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([2, 3, -2, 0, 4, 1, -3])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([-3, 0, 4, 1, 2, 3, -2])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([3, 4, 1, 2, -2, -3, 0])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([-2, 1, 2, -3, 0, 3, 4])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([0, 3, 4, -2, 1, 2, -3])'

    next(gps_it)
    assert str(gps.grove_linked_list) == 'deque([4, 0, 3, -2, 1, 2, -3])'

    with pytest.raises(StopIteration):
        next(gps_it)


def test_full():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process_other.GrovePositioningSystem(num_input)

    gps_it = iter(gps)

    for _ in gps_it:
        pass

    assert gps.get_key_nos() == 3


def test_full_with_decryption_key():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process_other.GrovePositioningSystem(num_input, apply_decryption_key=True, mix_number=10)
    assert str(gps.grove_linked_list) == 'deque([811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612])'

    gps_it = iter(gps)

    for _ in gps_it:
        pass

    gps.locate(gps.node_zero)
    assert str(gps.grove_linked_list) == 'deque([0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153])'

    assert gps.get_key_nos() == 1623178306

# todo intermediate states