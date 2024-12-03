from dataclasses import dataclass
from pathlib import Path
from pprint import pformat
from typing import Dict, List, Tuple


@dataclass
class Position:

    x: int
    y: int


class BingoBoard:
    def __init__(self, numbers: List[List[int]]) -> None:
        self._numbers = numbers

        self._numbers_to_positions: Dict[int, Position] = {}
        for y, row in enumerate(numbers):
            for x, number in enumerate(row):
                self._numbers_to_positions[number] = Position(x, y)

        # Mark each space as False to start, since none are marked
        self._marked = [[False] * len(numbers[0]) for _ in range(len(numbers))]

    def mark(self, number: int) -> None:
        # We can't mark since this board doesn't have this number
        if number not in self._numbers_to_positions:
            return

        position = self._numbers_to_positions[number]
        self._marked[position.y][position.x] = True

    @property
    def _has_horizontal_winner(self) -> bool:
        """Return True if a whole row is marked."""
        return any(all(row) for row in self._marked)

    @property
    def _has_vertical_winner(self) -> bool:
        """Return True if a whole column is marked."""

        def col_fully_marked(index: int) -> bool:
            return all(row[index] for row in self._marked)

        col_count = len(self._marked[0])
        return any(col_fully_marked(index) for index in range(col_count))

    @property
    def is_winner(self) -> bool:
        """
        Return True if this board is currently a winner.

        An entire row or column must be marked.
        """
        return self._has_horizontal_winner or self._has_vertical_winner

    @property
    def unmarked_sum(self) -> int:
        """Return the sum of the numbers that haven't been marked."""
        sum_ = 0

        for row_num, row in enumerate(self._numbers):
            for col_num, number in enumerate(row):
                if not self._marked[row_num][col_num]:
                    sum_ += number

        return sum_

    def __repr__(self) -> str:
        return pformat(self._numbers)


def get_input() -> Tuple[List[int], List[BingoBoard]]:
    input_path = Path(__file__).parent.joinpath("input.txt")

    with open(input_path, "r") as file:
        # Use `.strip` to remove "\n"
        lines = [l.strip() for l in file.readlines()]

    # The first line is the numbers that will be marked on the bingo boards.
    # They're separated by commas
    to_mark = [int(x) for x in lines[0].split(",")]

    # Keep track of the boards we'be parsed
    bingo_boards = []
    # Keep track of the lines that belong to the current board
    board_lines = []
    # The bingo boards don't start until the third line
    for line in lines[2:]:
        # If we hit an empty line, the previous lines we've parsed belong to
        # one board
        if not line:
            bingo_boards.append(BingoBoard(board_lines))
            board_lines = []
            continue

        # Parse the current line as a row in the board.
        # Don't pass anything to `split` since the default is to split by whitespace,
        # some numbers are separated by two spaces which is a bit frustrating
        board_lines.append([int(x) for x in line.split()])

    return to_mark, bingo_boards


to_mark, bingo_boards = get_input()


def part_1() -> int:
    for number in to_mark:
        for bingo_board in bingo_boards:
            bingo_board.mark(number)
            if bingo_board.is_winner:
                return bingo_board.unmarked_sum * number


print(part_1())


def part_2() -> int:
    # Keep track of the boards that haven't won yet
    remaining_boards = set(bingo_boards)

    for number in to_mark:
        # Keep track of the boards that won with this number
        newly_won = set()
        for bingo_board in remaining_boards:
            bingo_board.mark(number)
            if bingo_board.is_winner:
                newly_won.add(bingo_board)
                # We're going to remove all of the remaining boards, so this must have
                # been the last one
                if len(newly_won) == len(remaining_boards):
                    return bingo_board.unmarked_sum * number

        # Remove the boards we know are already winners so we don't have to
        # keep checking them
        remaining_boards.difference_update(newly_won)


print(part_2())
