# https://adventofcode.com/2021/day/14

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Tuple

from adventofcode.utils import load_list

lines = load_list()


def get_template_and_rules() -> Tuple[str, Dict[str, str]]:
    # The first line is the template, the rules start on line 3.
    # Each rule looks like `CH -> B`
    return lines[0], dict(l.split(" -> ") for l in lines[2:])


template, rules = get_template_and_rules()


def process_slow(polymer: str, rules: Dict[str, str]) -> str:
    """
    Process one step of `polymer` with `rules`.

    This is the slow solution found before part 2 necessitated it being much faster.
    """
    # Map index to char to insert
    insertions = {}

    for index, pair in enumerate(zip(polymer, polymer[1:])):
        pair = "".join(pair)

        # If this pair is in the rules, note that we have to insert its replacement
        if pair in rules:
            # If we have
            #   `...AB...`
            # We'll insert between A and B (i.e. index + 1)
            #   `...AxB...`
            # If we've already had previous insertions, the new index is shifted right
            # by that many places
            insertions[index + 1 + len(insertions)] = rules[pair]

    # Allocate space for the new polymer. The size is the old size plus the number of
    # insertions
    new_polymer = [None] * (len(polymer) + len(insertions))
    # Where are we in the old polymer?
    old_index = 0
    for new_index in range(len(new_polymer)):
        if new_index in insertions:
            # If we have something to insert here, insert it
            new_polymer[new_index] = insertions[new_index]
        else:
            # Otherwise, insert the char from the old polymer
            new_polymer[new_index] = polymer[old_index]
            old_index += 1

    return "".join(new_polymer)


def process(polymer: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    """
    Process one step of `polymer` with `rules`.

    This is the much faster solution found for part 2.

    The general idea is that we don't actually care about the order of the chars, so we
    don't have to store the entire polymer. We only need to know the pairs and their
    counts to know what we'll insert in the next step.

    "NNCB" -> {
        "NN": 1,
        "NC": 1,
        "CB": 1,
    }

    If we have the pair "NN" and it needs "C" inserted, we need to remove all "NN"s and
    add the same number of "NC" and "CN" pairs.
    """
    updates = defaultdict(int)

    for pair, insertion in rules.items():
        if pair not in polymer:
            continue

        count = polymer[pair]
        # Remove all occurences of this pair, since the new char will split it
        updates[pair] -= count

        # If we have "NN" and insert "C", we'll end up with "NC" and "CN"
        new_pair_a = f"{pair[0]}{insertion}"
        new_pair_b = f"{insertion}{pair[1]}"

        # We create the same number of each new pair as we had of the old pair
        updates[new_pair_a] += count
        updates[new_pair_b] += count

    # Copy the polymer pairs, defaulting new counts to 0.
    # Remember we need to process the updates all at once at the end since all pairs are
    # considered simultaneously.
    polymer = defaultdict(int, polymer)
    for pair, count in updates.items():
        polymer[pair] += count

        # If the pair doesn't have any more occurences, remove it to keep the size of
        # the polymer down
        if polymer[pair] <= 0:
            del polymer[pair]

    return polymer


def simulate(steps: int) -> int:
    # Keep track of the last char in the template, see note below
    last = template[-1]
    # Create all pairs from the polymer.
    # For example, "NNCB" -> ["NN", "NC", "CB"]
    # Count the occurences of each
    polymer = Counter("".join(pair) for pair in zip(template, template[1:]))

    for _ in range(steps):
        polymer = process(polymer, rules)

    # Count how many times each char appears
    counts = defaultdict(int)
    for pair, count in polymer.items():
        # Since we duplicated chars, make sure to only count the first char in each
        # pair.
        # For example, "NNCB" -> ["NN", "NC", "CB"]
        # which would give us
        #   3 Ns, 2 Cs, and 1 B
        # even though the real counts are
        #   2 Ns, 1 C,  and 1 B
        # Only counting the first char in the pair removes the duplicates
        counts[pair[0]] += count

    # Since we're only looking at the first value in each pair, we don't count the last
    # char
    counts[last] += 1

    most_common = max(counts.values())
    least_common = min(counts.values())

    return most_common - least_common


def part_1() -> int:
    return simulate(10)


print(part_1())


def part_2() -> int:
    return simulate(40)


print(part_2())
