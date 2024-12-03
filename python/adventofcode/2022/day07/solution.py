from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, Iterator, Optional, Union

from adventofcode.utils import load_list


@dataclass
class File:

    name: str
    size: int
    parent: Dir


@dataclass
class Dir:

    name: str
    children: Dict[str, Union[File, Dir]] = field(default_factory=dict)
    parent: Optional[Dir] = None

    def add(self, file: Union[File, Dir]) -> None:
        self.children[file.name] = file

    def cd(self, name: str) -> Dir:
        return self.children[name]

    @cached_property
    def size(self) -> int:
        return sum(c.size for c in self.children.values())

    @property
    def all_children(self) -> Iterator[Union[File, Dir]]:
        for child in self.children.values():
            yield child

            if isinstance(child, Dir):
                yield from child.all_children


def get_filesystem() -> Dir:
    top_level = Dir(name="/")
    cur_dir = top_level
    commands = load_list(parser=lambda line: line.replace("$ ", "").split(" "))

    for command in commands:
        # ls
        if len(command) == 1:
            continue
        elif command[0] == "cd":
            if command[1] == "..":
                cur_dir = cur_dir.parent
            elif command[1] == "/":
                cur_dir = top_level
            else:
                cur_dir = cur_dir.cd(command[1])
        elif command[0] == "dir":
            cur_dir.add(Dir(name=command[1], parent=cur_dir))
        else:
            cur_dir.add(File(name=command[1], size=int(command[0]), parent=cur_dir))

    return top_level


def part_1() -> int:
    return sum(
        f.size
        for f in get_filesystem().all_children
        if isinstance(f, Dir) and f.size <= 100000
    )


print(part_1())


def part_2() -> int:
    fs = get_filesystem()
    unused = 70000000 - fs.size
    needed = 30000000 - unused

    return min(
        f.size for f in fs.all_children if isinstance(f, Dir) and f.size >= needed
    )


print(part_2())
