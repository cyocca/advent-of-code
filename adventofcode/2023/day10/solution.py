from collections import deque
from typing import Final

from adventofcode.utils import Direction, Point, get_area, load_list

PIPE_TO_DIRECTIONS: Final = {
    "|": {Direction.UP, Direction.DOWN},
    "-": {Direction.LEFT, Direction.RIGHT},
    "L": {Direction.UP, Direction.RIGHT},
    "J": {Direction.UP, Direction.LEFT},
    "7": {Direction.DOWN, Direction.LEFT},
    "F": {Direction.DOWN, Direction.RIGHT},
}


def get_grid() -> list[list[str]]:
    return load_list(parser=list)


def find_start(grid: list[list[str]]) -> Point:
    for row_index, row in enumerate(grid):
        for col_index, _ in enumerate(row):
            if grid[row_index][col_index] == "S":
                return Point(col_index, row_index)

    raise ValueError("Could not find starting point")


def find_starting_neighbors(grid: list[list[str]], start: Point) -> list[Point]:
    starting_neighbors = []

    for direction in Direction:
        neighbor_position = start.translate(*direction.value.as_tuple())
        neighbor_pipe = grid[neighbor_position.y][neighbor_position.x]

        if neighbor_pipe == ".":
            continue

        if any(
            neighbor_position.translate(*d.value.as_tuple()) == start
            for d in PIPE_TO_DIRECTIONS[neighbor_pipe]
        ):
            starting_neighbors.append(neighbor_position)

    assert len(starting_neighbors) == 2
    return starting_neighbors


def get_distance_to_farthest_loop_point() -> int:
    grid = get_grid()
    start = find_start(grid)
    starting_neighbors = find_starting_neighbors(grid, start)

    max_distance = 0
    seen = {start}
    to_process = deque(((1, n) for n in starting_neighbors))

    while to_process:
        distance, point = to_process.popleft()

        if point in seen:
            continue

        seen.add(point)

        max_distance = max(distance, max_distance)
        new_distance = distance + 1
        pipe = grid[point.y][point.x]

        to_process.extend(
            (new_distance, point.translate(*d.value.as_tuple()))
            for d in PIPE_TO_DIRECTIONS[pipe]
        )

    return max_distance


def part_1() -> int:
    return get_distance_to_farthest_loop_point()


def get_perimeter() -> list[Point]:
    grid = get_grid()
    start = find_start(grid)
    starting_neighbors = find_starting_neighbors(grid, start)

    perimeter = [start]
    last = start
    current = starting_neighbors.pop()

    while current != start:
        # We only want corners for the area formula.
        if grid[current.y][current.x] in {"L", "J", "7", "F"}:
            perimeter.append(current)

        pipe = grid[current.y][current.x]
        new_points = (
            current.translate(*d.value.as_tuple()) for d in PIPE_TO_DIRECTIONS[pipe]
        )
        # Make sure we don't go backwards
        last, current = current, next(p for p in new_points if p != last)

    return perimeter


def part_2() -> int:
    return get_area(get_perimeter())


print(part_1())
print(part_2())
