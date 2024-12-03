import operator
from collections import deque
from functools import reduce
from itertools import product
from typing import Iterable, Optional, Set, Tuple

from adventofcode.utils import load_list

height_map = load_list(parser=lambda line: [int(x) for x in line])


def height_at(x: int, y: int) -> Optional[int]:
    """
    Return the height at (x, y).

    If the point is invalid, return None
    """
    if x < 0:
        return None

    if len(height_map[0]) <= x:
        return None

    if y < 0:
        return None

    if len(height_map) <= y:
        return None

    return height_map[y][x]


def get_neighbors(x: int, y: int) -> Iterable[Tuple[int, int]]:
    """
    Return the neighbors of (x, y).

    This only includes top, bottom, left, and right (not diagonals)
    """
    return (
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y),
    )


def is_lowest(x: int, y: int) -> bool:
    """Return True if (x, y) is the lowest point of its neighbors."""
    height = height_map[y][x]

    for neighbor in get_neighbors(x, y):
        neighbor_height = height_at(*neighbor)

        if neighbor_height is not None and neighbor_height <= height:
            return False

    return True


def part_1() -> int:
    # Get all tuples of (x, y) in the height map
    points = product(range(len(height_map[0])), range(len(height_map)))

    return sum(1 + height_at(*point) for point in points if is_lowest(*point))


print(part_1())


def get_basin(unvisited: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Return the next unvisited basin."""
    # Keep track of all the points in the basin
    basin = set()
    # Pick a random point we haven't visited to start creating the basin
    start = next(iter(unvisited))
    # Keep track of the points in the basin we still need to visit
    to_visit = deque([start])

    while to_visit:
        x, y = to_visit.popleft()

        # If we've already been here, don't do anything
        if (x, y) not in unvisited:
            continue

        # Mark as visited
        unvisited.remove((x, y))

        # Don't visit neighbors of points with height 9. Otherwise we'll combine basins
        # that should be separate
        if height_map[y][x] == 9:
            continue

        # Add this point to the basin and mark its neighbors as points that need visited
        basin.add((x, y))
        to_visit.extend(get_neighbors(x, y))

    return basin


def part_2() -> int:
    # General strategy is
    #   1. Pick a random point in the height map
    #   2. BFS by visiting all neighbors and adding them to the basin if their height
    #      isn't 9
    #   3. When we've run out of points to visit, we've found the whole basin. Start
    #      over with a new random point we haven't visited (to find a new basin)
    #   4. When we've visited every point, we've found all the basins

    # Get all tuples of (x, y) in the height map
    unvisited = set(product(range(len(height_map[0])), range(len(height_map))))
    basin_sizes = []

    while unvisited:
        basin_sizes.append(len(get_basin(unvisited)))

    three_largest_basins = sorted(basin_sizes, reverse=True)[:3]
    # Multiply the three basin sizes together
    return reduce(operator.mul, three_largest_basins)


print(part_2())
