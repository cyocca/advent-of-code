import inspect
from pathlib import Path
from typing import Callable, List, Optional, TypeVar

_T = TypeVar("_T")


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

    # If a file path isn't provided, default to an "input.txt" file in the caller's
    # directory
    if not file_path:
        # Get the file that called this function. `stack[0]` is this function
        calling_module = inspect.stack()[1].filename
        # Get a path to the `input.txt` file in the callers parent dir
        file_path = Path(calling_module).parent.joinpath("input.txt")

    with open(file_path, "r") as file:
        # Use `.strip` to remove "\n"
        return [parser(l.strip()) for l in file.readlines()]
