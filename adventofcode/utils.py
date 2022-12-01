import inspect
from pathlib import Path
from typing import Callable, List, Optional, TypeVar

_T = TypeVar("_T")


def load_input(file_path: Optional[str] = None) -> str:
    # If a file path isn't provided, default to an "input.txt" file in the caller's
    # directory
    if not file_path:
        # Get the file that called this function. It will be the first one that's not
        # this file
        stack = iter(inspect.stack())
        calling_module = next(stack).filename

        while calling_module == __file__:
            calling_module = next(stack).filename

        # Get a path to the `input.txt` file in the callers parent dir
        file_path = Path(calling_module).parent.joinpath("input.txt")

    with open(file_path, "r") as file:
        return file.read().strip()


def load_list(
    file_path: Optional[str] = None, parser: Optional[Callable[[str], _T]] = None
) -> List[_T]:
    """
    Load a list of inputs from `file_path`.

    By default, load from the file "input.txt" in the caller's directory, since that's
    where the input is typically stored.

    If `parser` is provided, it will be called on each line of input from the file.
    """
    # No-op if a parser isn't given
    parser = parser or (lambda x: x)
    # Use `.strip` to remove last "\n"
    return [parser(l) for l in load_input(file_path).split("\n")]


def is_valid_point(x: int, y: int, grid: List[List]) -> bool:
    """
    Return True if (x, y) is a valid point.

    Essentially make sure it's not outside the bounds of `grid`
    """
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)
