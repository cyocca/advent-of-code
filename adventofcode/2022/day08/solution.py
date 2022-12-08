from pathlib import Path
from typing import List, Set, Tuple

from adventofcode.utils import load_list


def save_debug_map(
    heights: List[List[int]],
    visible_from_top: Set[Tuple[int, int]],
    visible_from_bottom: Set[Tuple[int, int]],
    visible_from_left: Set[Tuple[int, int]],
    visible_from_right: Set[Tuple[int, int]],
) -> None:
    for row in range(len(heights)):
        for col in range(len(heights[0])):
            if (row, col) in visible_from_top:
                marker = "t"
            elif (row, col) in visible_from_bottom:
                marker = "b"
            elif (row, col) in visible_from_left:
                marker = "l"
            elif (row, col) in visible_from_right:
                marker = "r"
            else:
                marker = heights[row][col]

            heights[row][col] = marker

    with open(Path(__file__).parent / "debug.txt", "w") as file:
        file.write("\n".join("".join(str(x) for x in row) for row in heights))


def get_heights() -> List[List[int]]:
    return load_list(parser=lambda line: [int(x) for x in line])


def find_visible_horizontally(
    heights: List[List[int]], invert: bool
) -> Set[Tuple[int, int]]:
    visible = set()
    if invert:
        direction = -1
        col_range = range(len(heights[0]) - 1, 0, direction)
    else:
        direction = 1
        col_range = range(0, len(heights[0]), direction)

    for row in range(len(heights)):
        tallest = -1
        for col in col_range:
            # This tree is only visible if it's taller than the tallest tree we've seen
            # so far
            if heights[row][col] > tallest:
                tallest = heights[row][col]
                visible.add((row, col))

    return visible


def find_visible_vertically(
    heights: List[List[int]], invert: bool
) -> Set[Tuple[int, int]]:
    visible = set()
    if invert:
        direction = -1
        row_range = range(len(heights) - 1, 0, direction)
    else:
        direction = 1
        row_range = range(0, len(heights), direction)

    for col in range(len(heights[0])):
        tallest = -1
        for row in row_range:
            if heights[row][col] > tallest:
                tallest = heights[row][col]
                visible.add((row, col))

    return visible


def part_1() -> int:
    heights = get_heights()

    visible_from_top = find_visible_vertically(heights, invert=False)
    visible_from_bottom = find_visible_vertically(heights, invert=True)
    visible_from_left = find_visible_horizontally(heights, invert=False)
    visible_from_right = find_visible_horizontally(heights, invert=True)

    # save_debug_map(
    #     heights,
    #     visible_from_top,
    #     visible_from_bottom,
    #     visible_from_left,
    #     visible_from_right,
    # )

    return len(
        {
            *visible_from_top,
            *visible_from_bottom,
            *visible_from_left,
            *visible_from_right,
        }
    )


print(part_1())


def find_vertical_view(
    heights: List[List[int]], row: int, col: int, invert: bool
) -> int:
    count = 0
    height = heights[row][col]

    if invert:
        at_end = lambda row: row >= len(heights)
        direction = 1
    else:
        at_end = lambda row: row < 0
        direction = -1

    row += direction
    while not at_end(row) and heights[row][col] < height:
        row += direction
        count += 1

    # Apparently we count the last tree, i.e. the one that blocks our view
    if not at_end(row):
        count += 1

    return count


def find_horizontal_view(
    heights: List[List[int]], row: int, col: int, invert: bool
) -> int:
    count = 0
    height = heights[row][col]

    if invert:
        at_end = lambda col: col >= len(heights[0])
        direction = 1
    else:
        at_end = lambda col: col < 0
        direction = -1

    col += direction
    while not at_end(col) and heights[row][col] < height:
        col += direction
        count += 1

    # Apparently we count the last tree, i.e. the one that blocks our view
    if not at_end(col):
        count += 1

    return count


def calculate_scenic_score(heights: List[List[int]], row: int, col: int) -> int:
    args = (heights, row, col)
    return (
        find_vertical_view(*args, invert=False)
        * find_vertical_view(*args, invert=True)
        * find_horizontal_view(*args, invert=False)
        * find_horizontal_view(*args, invert=True)
    )


def part_2() -> int:
    heights = get_heights()

    return max(
        calculate_scenic_score(heights, row, col)
        for row in range(len(heights))
        for col in range(len(heights[0]))
    )


print(part_2())
