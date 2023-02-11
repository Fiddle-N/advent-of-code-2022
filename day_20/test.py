from day_20 import process


def test_initial():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process.GrovePositioningSystem(num_input)

    assert gps.grove_nodes[0].prev == gps.grove_nodes[6]
    assert gps.grove_nodes[0].data == 1
    assert gps.grove_nodes[0].next == gps.grove_nodes[1]

    assert gps.grove_nodes[1].prev == gps.grove_nodes[0]
    assert gps.grove_nodes[1].data == 2
    assert gps.grove_nodes[1].next == gps.grove_nodes[2]

    assert gps.grove_nodes[2].prev == gps.grove_nodes[1]
    assert gps.grove_nodes[2].data == -3
    assert gps.grove_nodes[2].next == gps.grove_nodes[3]

    assert gps.grove_nodes[3].prev == gps.grove_nodes[2]
    assert gps.grove_nodes[3].data == 3
    assert gps.grove_nodes[3].next == gps.grove_nodes[4]

    assert gps.grove_nodes[4].prev == gps.grove_nodes[3]
    assert gps.grove_nodes[4].data == -2
    assert gps.grove_nodes[4].next == gps.grove_nodes[5]

    assert gps.grove_nodes[5].prev == gps.grove_nodes[4]
    assert gps.grove_nodes[5].data == 0
    assert gps.grove_nodes[5].next == gps.grove_nodes[6]

    assert gps.grove_nodes[6].prev == gps.grove_nodes[5]
    assert gps.grove_nodes[6].data == 4
    assert gps.grove_nodes[6].next == gps.grove_nodes[0]

    assert len(gps.grove_linked_list) == 7


def test_run():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process.GrovePositioningSystem(num_input)
    gps_it = iter(gps)

    next(gps_it)

    assert len(gps.grove_linked_list) == 7

    # 2
    # 1
    # -3
    # 3
    # -2
    # 0
    # 4

    assert gps.grove_nodes[1].prev == gps.grove_nodes[-1]
    assert gps.grove_nodes[1].data == 2
    assert gps.grove_nodes[1].next == gps.grove_nodes[0]

    assert gps.grove_nodes[0].prev == gps.grove_nodes[1]
    assert gps.grove_nodes[0].data == 1
    assert gps.grove_nodes[0].next == gps.grove_nodes[2]

    assert gps.grove_nodes[2].prev == gps.grove_nodes[0]
    assert gps.grove_nodes[2].data == -3
    assert gps.grove_nodes[2].next == gps.grove_nodes[3]

    next(gps_it)

    assert len(gps.grove_linked_list) == 7

    # 1
    # -3
    # 2
    # 3
    # -2
    # 0
    # 4

    assert gps.grove_nodes[0].prev == gps.grove_nodes[-1]
    assert gps.grove_nodes[0].data == 1
    assert gps.grove_nodes[0].next == gps.grove_nodes[2]

    assert gps.grove_nodes[2].prev == gps.grove_nodes[0]
    assert gps.grove_nodes[2].data == -3
    assert gps.grove_nodes[2].next == gps.grove_nodes[1]

    assert gps.grove_nodes[1].prev == gps.grove_nodes[2]
    assert gps.grove_nodes[1].data == 2
    assert gps.grove_nodes[1].next == gps.grove_nodes[3]

    next(gps_it)

    assert len(gps.grove_linked_list) == 7

    # 1
    # 2
    # 3
    # -2
    # -3
    # 0
    # 4

    assert gps.grove_nodes[0].prev == gps.grove_nodes[-1]
    assert gps.grove_nodes[0].data == 1
    assert gps.grove_nodes[0].next == gps.grove_nodes[1]

    assert gps.grove_nodes[1].prev == gps.grove_nodes[0]
    assert gps.grove_nodes[1].data == 2
    assert gps.grove_nodes[1].next == gps.grove_nodes[3]

    assert gps.grove_nodes[3].prev == gps.grove_nodes[1]
    assert gps.grove_nodes[3].data == 3
    assert gps.grove_nodes[3].next == gps.grove_nodes[4]

    assert gps.grove_nodes[4].prev == gps.grove_nodes[3]
    assert gps.grove_nodes[4].data == -2
    assert gps.grove_nodes[4].next == gps.grove_nodes[2]

    assert gps.grove_nodes[2].prev == gps.grove_nodes[4]
    assert gps.grove_nodes[2].data == -3
    assert gps.grove_nodes[2].next == gps.grove_nodes[5]

    assert gps.grove_nodes[5].prev == gps.grove_nodes[2]
    assert gps.grove_nodes[5].data == 0
    assert gps.grove_nodes[5].next == gps.grove_nodes[6]

    # todo full tests

def test_run_full():
    num_input = """\
1
2
-3
3
-2
0
4"""
    gps = process.GrovePositioningSystem(num_input)
    gps_it = iter(gps)

    for _ in gps_it:
        pass

    assert gps.get_key_nos() == 3