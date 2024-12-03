from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush
from typing import List

from adventofcode.utils import is_valid_point, load_list

risk_levels: List[List[int]] = load_list(parser=lambda l: [int(x) for x in l])


def get_risk(x: int, y: int, risk_levels: List[List[int]]) -> int:
    return risk_levels[y][x]


def repeat(risk_levels: List[List[int]]) -> List[List[int]]:
    """
    Repeat `risk_levels` to the right or downward.

    We only need one function since both operations are the same. Increase risk by 1
    and wrap it around if it's greater than 9.
    """
    original_height = len(risk_levels)
    original_width = len(risk_levels[0])

    new_map = deepcopy(risk_levels)

    for y in range(original_height):
        for x in range(original_width):
            new_map[y][x] = new_map[y][x] + 1

            if new_map[y][x] > 9:
                new_map[y][x] = 1

    return new_map


def expand(risk_levels: List[List[int]]) -> List[List[int]]:
    """
    Expand `risk_levels` into a 5x5 grid.

    i.e. repeat `risk_levels` right 5 times and down 5 times for a total of 25 tiles.

    Notice that the resulting grid is symmetric across a line from the top left to the
    bottom right. i.e. if we number each unique tile, they look like this

    - 0 1 2 3
    . - 4 5 6
    . . - 7 8
    . . . - 9
    . . . . -

    - . . . .
    0 - . . .
    1 4 - . .
    2 5 7 - .
    3 6 8 9 -
    """
    original_height = len(risk_levels)
    original_width = len(risk_levels[0])

    # 5x5 grid
    tiles = [[None] * 5 for _ in range(5)]

    # Create each tile in the 5x5 grid on the right half of the diagonal line mentioned
    # above
    for y in range(5):
        for x in range(y, 5):
            # The top left tile is the original risk levels
            if (x, y) == (0, 0):
                tiles[y][x] = risk_levels
                continue

            # If we're on the top row, we can just repeat the tile to the left of us
            if y == 0:
                tiles[y][x] = repeat(tiles[y][x - 1])
                continue

            # Otherwise, repeat the tile above us
            tiles[y][x] = repeat(tiles[y - 1][x])

    # Copy the tiles on the left half of the diagonal line mentioned above from the
    # right half we already filled in
    for y in range(1, 5):
        for x in range(y):
            tiles[y][x] = tiles[x][y]

    new_height = original_height * 5
    new_width = original_width * 5
    new_risk_levels = [[None] * new_width for _ in range(new_height)]

    # Flatten out the list of lists of tiles into a single 2D grid
    for tiles_y, tile_row in enumerate(tiles):
        for tiles_x, tile in enumerate(tile_row):
            for y, row in enumerate(tile):
                for x, value in enumerate(row):
                    # To get the absolute y, multiply the tile row by the height of
                    # each tile and add our position within the tile
                    new_y = y + (original_height * tiles_y)
                    new_x = x + (original_width * tiles_x)
                    new_risk_levels[new_y][new_x] = value

    return new_risk_levels


@dataclass
class Path:

    x: int
    y: int
    risk: int

    # Implement for comparison in the heap
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Path):
            return NotImplemented

        return self.risk < other.risk


def get_risk_of_lowest_path(risk_levels: List[List[int]]) -> int:
    """
    Find the risk of the lowest risk path.

    Use Dijkstra
    """
    # Start with a path that has 0 risk and is at position (0, 0)
    paths = [Path(0, 0, 0)]
    # Keep track of the positions we've visited so we don't visit twice
    visited = set()
    # We stop when we reach the bottom right position
    end_pos = (len(risk_levels[0]) - 1, len(risk_levels) - 1)

    while True:
        # Get the path with the lowest risk
        path = heappop(paths)

        # Consider each neighbor (up, down, left, right)
        for point in (
            (path.x + 1, path.y),
            (path.x - 1, path.y),
            (path.x, path.y + 1),
            (path.x, path.y - 1),
        ):
            # We can't visit if the point isn't in the grid or we've already visited
            if not is_valid_point(*point, risk_levels) or point in visited:
                continue

            new_risk = path.risk + get_risk(*point, risk_levels)

            # If this is the end, we've found the lowest risk since we always consider
            # the next path with the lowest risk
            if point == end_pos:
                return new_risk

            # Make sure not to come back here
            visited.add(point)
            # Add this new path to those we may consider. Use a heap so the paths are
            # ordered by risk (from lowest to highest)
            heappush(paths, Path(*point, new_risk))


def part_1() -> int:
    return get_risk_of_lowest_path(risk_levels)


print(part_1())


def part_2() -> int:
    return get_risk_of_lowest_path(expand(risk_levels))


print(part_2())
