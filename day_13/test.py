import pytest

from day_13 import process
from day_13.process import Packet


@pytest.mark.parametrize(
    "packets",
    [
        (
            Packet([1]),
            Packet([2]),
        ),
        (
            Packet([Packet([1])]),
            Packet([2]),
        ),
        (
            Packet([1]),
            Packet([Packet([2])]),
        ),
        (
            Packet([1]),
            Packet([1, 1]),
        ),
        (
            Packet([1, 1]),
            Packet([2]),
        ),
        (
            Packet([]),
            Packet([1]),
        ),
        (
            Packet([]),
            Packet([Packet([1])]),
        ),
        (
            Packet([]),
            Packet([Packet([])]),
        ),
    ],
)
def test_packets_different(packets):
    left_packet, right_packet = packets

    assert (left_packet < right_packet) == True
    assert (right_packet > left_packet) == True

    assert (left_packet > right_packet) == False
    assert (right_packet < left_packet) == False


@pytest.mark.parametrize(
    "packets",
    [
        (
            Packet([1]),
            Packet([1]),
        ),
        (
            Packet([Packet([1])]),
            Packet([1]),
        ),
        (
            Packet([1, 1]),
            Packet([1, 1]),
        ),
        (
            Packet([]),
            Packet([]),
        ),
        (
            Packet([Packet([])]),
            Packet([Packet([])]),
        ),
    ],
)
def test_packets_equal(packets):
    left_packet, right_packet = packets

    assert (left_packet < right_packet) == False
    assert (right_packet > left_packet) == False

    assert (left_packet > right_packet) == False
    assert (right_packet < left_packet) == False


def test_full_distress_signal_valid_pairs():
    signal_input = """\
[1, 1, 3, 1, 1]
[1, 1, 5, 1, 1]

[[1], [2, 3, 4]]
[[1], 4]

[9]
[[8, 7, 6]]

[[4, 4], 4, 4]
[[4, 4], 4, 4, 4]

[7, 7, 7, 7]
[7, 7, 7]

[]
[3]

[[[]]]
[[]]

[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
"""
    signal = process.DistressSignal(signal_input)
    assert signal.valid_pkt_pair_idxs() == [1, 2, 4, 6]
    assert signal.sum_valid_pair_idx() == 13


def test_full_distress_signal_sorted():
    signal_input = """\
[1, 1, 3, 1, 1]
[1, 1, 5, 1, 1]

[[1], [2, 3, 4]]
[[1], 4]

[9]
[[8, 7, 6]]

[[4, 4], 4, 4]
[[4, 4], 4, 4, 4]

[7, 7, 7, 7]
[7, 7, 7]

[]
[3]

[[[]]]
[[]]

[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
"""

    signal = process.DistressSignal(signal_input)

    assert (
        "\n".join([str(pkt) for pkt in signal.sig])
        == """\
[]
[[]]
[[[]]]
[1, 1, 3, 1, 1]
[1, 1, 5, 1, 1]
[[1], [2, 3, 4]]
[1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
[1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
[[1], 4]
[[2]]
[3]
[[4, 4], 4, 4]
[[4, 4], 4, 4, 4]
[[6]]
[7, 7, 7]
[7, 7, 7, 7]
[[8, 7, 6]]
[9]"""
    )

    assert signal.find_decoder_key() == 140
