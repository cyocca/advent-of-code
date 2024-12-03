from itertools import combinations

from adventofcode.utils import Point, load_list


def get_grid() -> list[list[str]]:
    return load_list(parser=list)


def get_galaxy_locations(grid: list[list[str]]) -> list[Point]:
    locations = []

    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == "#":
                locations.append(Point(col_index, row_index))

    return locations


def get_empty_rows(grid: list[list[str]]) -> list[int]:
    empty_rows = []

    for row_index, row in enumerate(grid):
        if all(v == "." for v in row):
            empty_rows.append(row_index)

    return empty_rows


def get_empty_cols(grid: list[list[str]]) -> list[int]:
    empty_cols = []

    for col_index, _ in enumerate(grid[0]):
        if all(row[col_index] == "." for row in grid):
            empty_cols.append(col_index)

    return empty_cols


def get_distance(
    a: Point,
    b: Point,
    empty_rows: list[int],
    empty_cols: list[int],
    expansion_factor: int,
) -> int:
    expansion_distance = expansion_factor - 1
    # The distance is just how many times we need to go left/right and up/down
    distance = abs(a.y - b.y) + abs(a.x - b.x)

    # If an empty row comes between the two galaxies we're considering, add the
    # expansion factor
    for row in empty_rows:
        if min(a.y, b.y) < row < max(a.y, b.y):
            distance += expansion_distance

    for col in empty_cols:
        if min(a.x, b.x) < col < max(a.x, b.x):
            distance += expansion_distance

    return distance


def sum_galaxy_pair_distances(expansion_factor: int) -> int:
    grid = get_grid()
    galaxy_locations = get_galaxy_locations(grid)
    empty_rows = get_empty_rows(grid)
    empty_cols = get_empty_cols(grid)

    # Sum the distances for every pair of galaxies
    return sum(
        get_distance(*c, empty_rows, empty_cols, expansion_factor)
        for c in combinations(galaxy_locations, 2)
    )


def part_1() -> int:
    return sum_galaxy_pair_distances(expansion_factor=2)


def part_2() -> int:
    return sum_galaxy_pair_distances(expansion_factor=1_000_000)


print(part_1())
print(part_2())
