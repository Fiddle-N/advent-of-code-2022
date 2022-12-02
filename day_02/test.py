import pytest

from day_02 import process


@pytest.mark.parametrize(
    "round_input,opponent_move,your_move,total_score",
    [
        ('A X', process.RPSShapes.ROCK, process.RPSShapes.ROCK, 4),
        ('A Y', process.RPSShapes.ROCK, process.RPSShapes.PAPER, 8),
        ('A Z', process.RPSShapes.ROCK, process.RPSShapes.SCISSORS, 3),
        ('B X', process.RPSShapes.PAPER, process.RPSShapes.ROCK, 1),
        ('B Y', process.RPSShapes.PAPER, process.RPSShapes.PAPER, 5),
        ('B Z', process.RPSShapes.PAPER, process.RPSShapes.SCISSORS, 9),
        ('C X', process.RPSShapes.SCISSORS, process.RPSShapes.ROCK, 7),
        ('C Y', process.RPSShapes.SCISSORS, process.RPSShapes.PAPER, 2),
        ('C Z', process.RPSShapes.SCISSORS, process.RPSShapes.SCISSORS, 6),
    ]
)
def test_total_score_one_rounds_right_column_mode_move(round_input, opponent_move, your_move, total_score):
    encrypted_strategy_guide = f"""\
{round_input}
"""
    rps = process.RockPaperScissors(encrypted_strategy_guide, right_column_mode='move')
    assert len(rps.strategy_guide) == 1
    round = rps.strategy_guide[0]

    assert round.opponent_move == opponent_move
    assert round.your_move == your_move
    assert rps.total_score == total_score


def test_total_score_multiple_rounds_right_column_mode_move():
    encrypted_strategy_guide = """\
A Y
B X
C Z
"""
    rps = process.RockPaperScissors(encrypted_strategy_guide, right_column_mode='move')
    assert [
        (round.your_move.value + round.outcome.value)
        for round in rps.strategy_guide
    ] == [8, 1, 6]
    assert rps.total_score == 15


@pytest.mark.parametrize(
    "round_input,opponent_move,outcome,total_score",
    [
        ('A X', process.RPSShapes.ROCK, process.RPSScores.LOSS, 3),
        ('A Y', process.RPSShapes.ROCK, process.RPSScores.DRAW, 4),
        ('A Z', process.RPSShapes.ROCK, process.RPSScores.WIN, 8),
        ('B X', process.RPSShapes.PAPER, process.RPSScores.LOSS, 1),
        ('B Y', process.RPSShapes.PAPER, process.RPSScores.DRAW, 5),
        ('B Z', process.RPSShapes.PAPER, process.RPSScores.WIN, 9),
        ('C X', process.RPSShapes.SCISSORS, process.RPSScores.LOSS, 2),
        ('C Y', process.RPSShapes.SCISSORS, process.RPSScores.DRAW, 6),
        ('C Z', process.RPSShapes.SCISSORS, process.RPSScores.WIN, 7),
    ]
)
def test_total_score_one_rounds_right_column_mode_outcome(round_input, opponent_move, outcome, total_score):
    encrypted_strategy_guide = f"""\
{round_input}
"""
    rps = process.RockPaperScissors(encrypted_strategy_guide, right_column_mode='outcome')
    assert len(rps.strategy_guide) == 1
    round = rps.strategy_guide[0]

    assert round.opponent_move == opponent_move
    assert round.outcome == outcome
    assert rps.total_score == total_score


def test_total_score_multiple_rounds_right_column_mode_outcome():
    encrypted_strategy_guide = """\
A Y
B X
C Z
"""
    rps = process.RockPaperScissors(encrypted_strategy_guide, right_column_mode='outcome')
    assert [
        (round.your_move.value + round.outcome.value)
        for round in rps.strategy_guide
    ] == [4, 1, 7]
    assert rps.total_score == 12
