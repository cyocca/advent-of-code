from adventofcode.utils import load_input, Point, is_valid_point

def get_accessible_rolls(grid: list[list[str]]) -> set[Point]:
    can_be_accessed = set()

    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            point = Point(x, y)

            if col == '.':
                continue

            count = 0
            for neighbor in point.neighbors:
                if not is_valid_point(*neighbor.as_tuple(), grid):
                    continue

                if grid[neighbor.y][neighbor.x] == '@':
                    count += 1

            if count < 4:
                can_be_accessed.add(point)

    return can_be_accessed

def remove_rolls(grid: list[list[str]], accessible: set[Point]) -> None:
    for roll in accessible:
        grid[roll.y][roll.x] = '.'

def part1():
    grid = [list(r) for r in load_input().splitlines()]
    return len(get_accessible_rolls(grid))

def part2():
    grid = [list(r) for r in load_input().splitlines()]
    removed = 0

    while accessible_rolls := get_accessible_rolls(grid):
        remove_rolls(grid, accessible_rolls)
        removed += len(accessible_rolls)

    return removed


print(part1())
print(part2())
