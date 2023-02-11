from day_19 import process



def test_test_blueprint_1():
    blueprint_input = """\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian."""

    nme = process.NotEnoughMaterials(blueprint_input, line_wrapped=True)
    assert nme.find_quality_level() == 9


def test_test_blueprint_32_mins():
    blueprint_input = """\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian."""

    nme = process.NotEnoughMaterials(blueprint_input, line_wrapped=True)
    assert nme.find_quality_level(32) == 56


def test_test_blueprint_2():
    blueprint_input = """\
Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian."""

    nme = process.NotEnoughMaterials(blueprint_input, line_wrapped=True)
    assert nme.find_quality_level() == 24


def test_test_blueprints():
    blueprint_input = """\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian."""

    nme = process.NotEnoughMaterials(blueprint_input, line_wrapped=True)
    assert nme.find_quality_level() == 33
