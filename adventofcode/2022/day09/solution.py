from pathlib import Path
from typing import List, Tuple

from adventofcode.utils import load_list


def save_debug_map(
    ropes: List[List[Tuple[int, int]]],
) -> None:
    grids = []
    for rope in ropes:
        grid = [["."] * 50 for _ in range(50)]

        for index, (x, y) in enumerate(rope):
            grid[50 - (12 + y)][12 + x] = index

        grids.append("\n".join("".join(str(x) for x in row) for row in grid))

    with open(Path(__file__).parent / "debug.txt", "w") as file:
        file.write("\n\n".join(grids))


def get_moves() -> List[Tuple[str, int]]:
    moves = load_list(parser=lambda line: line.split(" "))

    return [(_, int(x)) for _, x in moves]


def simulate_rope(size: int) -> int:
    visited = set()
    # Head is at 0, tail is at the end
    rope = [(0, 0)] * size

    for direction, count in get_moves():
        for _ in range(count):
            x, y = rope[0]
            if direction == "U":
                new_head = (x, y + 1)
            elif direction == "R":
                new_head = (x + 1, y)
            elif direction == "D":
                new_head = (x, y - 1)
            elif direction == "L":
                new_head = (x - 1, y)
            else:
                raise ValueError(f"invalid direction `{direction}`")

            for index in range(len(rope)):
                # We always update the head
                if index == 0:
                    rope[0] = new_head
                    continue

                knot, new_knot = rope[index], rope[index - 1]
                x, y = knot
                new_x, new_y = new_knot

                if abs(x - new_x) == 2:
                    if new_x - x == 2:
                        # New one is right two, move right
                        knot = (x + 1, y)
                    else:
                        # New one is left two, move left
                        knot = (x - 1, y)

                    x, y = knot

                    # If it was also up, move up
                    if new_y - y >= 1:
                        knot = (x, y + 1)

                    # If it was also down, move down
                    if y - new_y >= 1:
                        knot = (x, y - 1)
                elif abs(y - new_y) == 2:
                    if new_y - y == 2:
                        # New one is up two, move up
                        knot = (x, y + 1)
                    else:
                        # New one is down two, move down
                        knot = (x, y - 1)

                    x, y = knot

                    # If it was also right, move right
                    if new_x - x >= 1:
                        knot = (x + 1, y)

                    # If it was also left, move left
                    if x - new_x >= 1:
                        knot = (x - 1, y)

                rope[index] = knot

            # Keep track of where the tail has been
            visited.add(rope[-1])

    return len(visited)


def part_1() -> int:
    return simulate_rope(size=2)


print(part_1())


def part_2() -> int:
    return simulate_rope(size=10)


print(part_2())
