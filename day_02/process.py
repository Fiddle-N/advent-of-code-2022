import enum
import dataclasses


class RPSShapes(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RPSScores(enum.Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


OPPONENT_MOVES = {
    'A': RPSShapes.ROCK,
    'B': RPSShapes.PAPER,
    'C': RPSShapes.SCISSORS
}

SELF_MOVES = {
    'X': RPSShapes.ROCK,
    'Y': RPSShapes.PAPER,
    'Z': RPSShapes.SCISSORS
}

OUTCOMES = {
    'X': RPSScores.LOSS,
    'Y': RPSScores.DRAW,
    'Z': RPSScores.WIN
}


@dataclasses.dataclass(frozen=True)
class RoundPart1:
    opponent_move: RPSShapes
    your_move: RPSShapes

    SHAPE_RELATIONSHIPS = [
        (RPSShapes.ROCK, RPSShapes.PAPER),
        (RPSShapes.PAPER, RPSShapes.SCISSORS),
        (RPSShapes.SCISSORS, RPSShapes.ROCK),
    ]

    @property
    def outcome(self) -> RPSScores:
        if self.opponent_move == self.your_move:
            return RPSScores.DRAW
        elif (self.opponent_move, self.your_move) in self.SHAPE_RELATIONSHIPS:
            return RPSScores.WIN
        elif (self.your_move, self.opponent_move) in self.SHAPE_RELATIONSHIPS:
            return RPSScores.LOSS
        else:
            return RPSScores.LOSS


@dataclasses.dataclass(frozen=True)
class RoundPart2:
    opponent_move: RPSShapes
    outcome: RPSScores

    @property
    def your_move(self) -> RPSShapes:
        if self.outcome == RPSScores.DRAW:
            return self.opponent_move
        elif (self.opponent_move, self.outcome) in (
            (RPSShapes.PAPER, RPSScores.LOSS),
            (RPSShapes.SCISSORS, RPSScores.WIN),
        ):
            return RPSShapes.ROCK
        elif (self.opponent_move, self.outcome) in (
            (RPSShapes.ROCK, RPSScores.WIN),
            (RPSShapes.SCISSORS, RPSScores.LOSS),
        ):
            return RPSShapes.PAPER
        elif (self.opponent_move, self.outcome) in (
            (RPSShapes.ROCK, RPSScores.LOSS),
            (RPSShapes.PAPER, RPSScores.WIN),
        ):
            return RPSShapes.SCISSORS
        else:
            raise Exception('Unexpected outcome')


class RockPaperScissors:

    def __init__(self, encrypted_strategy_guide: str, right_column_mode='move'):
        self.strategy_guide: list[RoundPart1] = []
        for round_txt in encrypted_strategy_guide.splitlines():
            round_choices = round_txt.split()
            assert len(round_choices) == 2
            if right_column_mode == 'move':
                round = RoundPart1(
                    opponent_move=OPPONENT_MOVES[round_choices[0]],
                    your_move=SELF_MOVES[round_choices[1]]
                )
            elif right_column_mode == 'outcome':
                round = RoundPart2(
                    opponent_move=OPPONENT_MOVES[round_choices[0]],
                    outcome=OUTCOMES[round_choices[1]]
                )
            else:
                raise Exception('unexpected param')
            self.strategy_guide.append(round)

    @property
    def total_score(self):
        return sum((round.your_move.value + round.outcome.value) for round in self.strategy_guide)


def read_file():
    with open('input.txt') as f:
        return f.read()


def main():
    file_txt = read_file()
    rps_right_column_mode_move = RockPaperScissors(file_txt, right_column_mode='move')
    print('Total score when right column is move:', rps_right_column_mode_move.total_score)
    rps_right_column_mode_outcome = RockPaperScissors(file_txt, right_column_mode='outcome')
    print('Total score when right column is outcome:', rps_right_column_mode_outcome.total_score)


if __name__ == '__main__':
    import timeit
    print(timeit.timeit(main, number=1))