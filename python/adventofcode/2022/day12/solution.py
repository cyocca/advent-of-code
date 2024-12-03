import sys
from collections import deque
from typing import List, Set, Tuple

from adventofcode.utils import load_list


def get_heights() -> List[str]:
    return load_list()


def find_positions_of_char(heights: List[str], char: str) -> Set[Tuple[int, int]]:
    positions = set()

    for row in range(len(heights)):
        for col in range(len(heights[0])):
            if heights[row][col] == char:
                positions.add((row, col))

    return positions


def find_steps(heights: List[str], start: Tuple[int, int]) -> int:
    end = find_positions_of_char(heights, "E").pop()
    to_visit = deque([(*start, 0)])
    visited = {start}

    while to_visit:
        row, col, steps = to_visit.popleft()
        cur = (row, col)

        if cur == end:
            return steps

        height = heights[row][col]

        for y, x in (
            (1, 0),  # up
            (0, 1),  # right
            (-1, 0),  # down
            (0, -1),  # left
        ):
            new_row = row + y
            new_col = col + x

            if new_row < 0 or new_row >= len(heights):
                continue

            if new_col < 0 or new_col >= len(heights[0]):
                continue

            new_height = heights[new_row][new_col]

            # Don't visit again
            if (new_row, new_col) in visited:
                continue

            # We have to be on a "z" to finish the path
            if new_height == "E" and height != "z":
                continue

            # From start we can go anywhere. Otherwise, make sure the new height is at
            # most one more
            if height == "S" or ord(new_height) - ord(height) <= 1:
                to_visit.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))

    # If we can't find a path, return a huge value
    return sys.maxsize


def find_min_steps_from_starting_char(starting_char: str) -> int:
    heights = get_heights()
    starts = find_positions_of_char(heights, starting_char)

    return min(find_steps(heights, s) for s in starts)


def part_1() -> int:
    return find_min_steps_from_starting_char("S")


print(part_1())


def part_2() -> int:
    return find_min_steps_from_starting_char("a")


print(part_2())
