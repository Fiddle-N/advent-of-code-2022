import pytest

from day_25 import process


@pytest.mark.parametrize(
    "dec, snafu",
    [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ],
)
def test_dec_snafu_conversion_brochure_numbers(dec, snafu):
    assert process.dec_to_snaf(dec) == snafu
    assert process.snaf_to_dec(snafu) == dec



@pytest.mark.parametrize(
    "snafu, dec",
    [
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37),
    ],
)
def test_snafu_to_dec_conversion_example(snafu, dec):
    assert process.snaf_to_dec(snafu) == dec


def test_dec_to_snafu_conversion_example():
    assert process.dec_to_snaf(4890) == "2=-1=0"


def test_calculate_fuel_requirement():
    reqs = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
    assert process.calc_fuel_requirement(reqs) == "2=-1=0"