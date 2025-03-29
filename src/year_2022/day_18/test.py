from day_18 import process


def test_simple():
    input_ = """\
1,1,1
2,1,1"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_surface_area() == 10


def test_larger():
    input_ = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_surface_area() == 64


def test_cube_with_droplet_inside():
    input_ = """\
2,2,2
3,2,2
4,2,2
2,3,2
3,3,2
4,3,2
2,4,2
3,4,2
4,4,2
2,2,3
3,2,3
4,2,3
2,3,3
4,3,3
2,4,3
3,4,3
4,4,3
2,2,4
3,2,4
4,2,4
2,3,4
3,3,4
4,3,4
2,4,4
3,4,4
4,4,4
"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_external_surface_area() == 54


def test_plus_cube_with_droplet_inside():
    input_ = """\
3,3,2
3,2,3
2,3,3
4,3,3
3,4,3
3,3,4
"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_external_surface_area() == 30


def test_plus_cube_with_droplet_with_zero_and_negative_coords():
    input_ = """\
0,0,-1
0,-1,0
-1,0,0
1,0,0
0,1,0
0,0,1
"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_external_surface_area() == 30


def test_larger_external_surface_area():
    input_ = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
    bb = process.BoilingBoulders(input_)
    assert bb.calculate_external_surface_area() == 58