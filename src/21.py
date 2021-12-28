from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import utils


class DeterministicDie:
    times_rolled: int = 0
    next_roll: int = 1

    def roll(self) -> int:
        roll = self.next_roll
        self.times_rolled += 1
        self.next_roll = self.next_roll % 100 + 1
        return roll


@dataclass
class Player:
    id: int
    space: int
    score: int = 0

    def __hash__(self):
        return hash((self.score, self.space))

    def __str__(self):
        return f"({self.space}, {self.score})"


@dataclass
class Game:
    player_1: Player
    player_2: Player

    def take_turn(self, roll: int) -> Game:
        new_space = (self.player_1.space - 1 + roll) % 10 + 1
        return Game(
            player_1=Player(id=self.player_2.id, space=self.player_2.space, score=self.player_2.score),
            player_2=Player(id=self.player_1.id, space=new_space, score=self.player_1.score + new_space),
        )

    def finished(self, max_score: int) -> bool:
        return self.player_1.score >= max_score or self.player_2.score >= max_score

    def __hash__(self):
        return hash((self.player_1, self.player_2))

    def __str__(self):
        return f"[{self.player_1}, {self.player_2}]"


def part_one(path: Path) -> int:
    lines = utils.read_lines(path)

    die: DeterministicDie = DeterministicDie()

    player_1: Player = Player(id=1, space=int(lines[0].split(": ")[1]))
    player_2: Player = Player(id=2, space=int(lines[1].split(": ")[1]))
    game = Game(player_1=player_1, player_2=player_2)

    while not game.finished(max_score=1000):
        roll = die.roll() + die.roll() + die.roll()
        game = game.take_turn(roll)
    return die.times_rolled * game.player_1.score


def part_two(path: Path) -> int:
    lines = utils.read_lines(path)

    dirac_die = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    player_1: Player = Player(id=1, space=int(lines[0].split(": ")[1]))
    player_2: Player = Player(id=2, space=int(lines[1].split(": ")[1]))
    games: dict[Game, int] = {Game(player_1=player_1, player_2=player_2): 1}

    winning_universes: dict[int, int] = {1: 0, 2: 0}
    while games:
        new_games: dict[Game, int] = {}
        for game in games:
            for roll in dirac_die:
                new_game = game.take_turn(roll)
                if new_game.finished(max_score=21):
                    winning_universes[new_game.player_2.id] += games[game] * dirac_die[roll]
                else:
                    if new_game not in new_games:
                        new_games[new_game] = 0
                    new_games[new_game] += games[game] * dirac_die[roll]
        games = new_games
    return max(winning_universes.values())


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "21.txt"
    print("Part 1:")
    print(part_one(input_path))
    print("Part 2:")
    print(part_two(input_path))
