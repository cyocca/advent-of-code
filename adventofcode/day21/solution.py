from dataclasses import InitVar, dataclass, field
from copy import deepcopy
from typing import List, Final, Set, Tuple
from itertools import product
from collections import defaultdict
from pprint import pformat

SPACES: Final = 10

@dataclass(eq=False)
class Chain:

    starting_position: InitVar[int]

    positions: List[int] = field(init=False)
    moves: List[int] = field(init=False, default_factory=list)
    score: int = field(init=False, default=0)

    def __post_init__(self, starting_position: int) -> None:
        self.positions = [starting_position]

    @property
    def cur_position(self) -> int:
        return self.positions[-1]

    def move(self, spaces: int) -> None:
        new_pos = (self.cur_position + spaces) % SPACES

        # Make sure 10 stays 10 because the position is 1-indexed
        if new_pos == 0:
            new_pos = 10

        self.score += new_pos
        self.positions.append(new_pos)
        self.moves.append(spaces)

    def __eq__(self, other: object) -> bool:
        return (self.positions, self.moves, self.score) == (other.positions, other.moves, other.score)

    def __hash__(self) -> int:
        return hash((*self.positions, *self.moves, self.score))

# We need permutations with replacement, i.e. every order of every roll including 1, 2,
# and 3
pairs_of_rolls = list(product(range(1, 4), repeat=3))
# Possibilities for how many spaces we can move
moves = {sum(p) for p in pairs_of_rolls}

# The number of spaces we move to the number of ways we end up moving that many spaces
# i.e. how many pairs of rolls make us move that many spaces
move_to_ways = defaultdict(int)
for pair in pairs_of_rolls:
    move_to_ways[sum(pair)] += 1

def get_winning_chains(
    chain1: Chain,
    chain2: Chain,
    winning_score: int,
) -> None:
    winning_chains = []
    # winning_chains = set()
    for move in moves:
        _get_winning_chains(move, chain1, chain2, winning_score, winning_chains, set())
    return winning_chains

def _get_winning_chains(
    move: int,
    chain1: Chain,
    chain2: Chain,
    winning_score: int,
    winning_chains: List[Chain],
    # Player 1 first
    cache: Set[Tuple[int, int, int, int]],
    turn: bool = True,
) -> None:
    key = (chain1.score, chain1.cur_position, chain2.score, chain2.cur_position, move, turn)

    if key in cache:
        # breakpoint()
        return

    cache.add(key)

    if turn:
        chain = deepcopy(chain1)
    else:
        chain = deepcopy(chain2)

    chain.move(move)

    if chain.score >= winning_score:
        winning_chains.append(chain)
        # if chain in winning_chains:
        #     breakpoint()
        # winning_chains.add(chain)
        return

    if turn:
        chains = (chain, chain2)
    else:
        chains = (chain1, chain)

    for move in moves:
        _get_winning_chains(move, *chains, winning_score, winning_chains, cache, not turn)

all_chains = get_winning_chains(Chain(4), Chain(8), 21)

# use `spaces_moved_to_ways` to map each chain ^ to the number of ways that chain can occur.
# For example 1 -> 4 -> 9 -> ...
# you move 3 (1 possible way) then 5 (2 possible ways) so the number of ways to create
# that chain so far is 1 * 2 = 2
# When we find the total number of ways to make the chains, we can divide each players
# number of winning chains by the total number of chains

print(f"number of chains: {len(all_chains)}")

def ways_to_make_chain(chain):
    ways_to_make_chain = 1

    for move in chain.moves:
        ways_to_make_chain *= move_to_ways[move]

    return ways_to_make_chain

# number_of_universes = 0

# for chain in all_chains:
#     ways_to_make_chain = 1

#     for moved in (space.spaces_moved for space in chain[1:]):
#         ways_to_make_chain *= spaces_moved_to_ways[moved]

#     moves = len(chain) - 1
#     # Three rolls per move
#     rolls = 3 * moves
#     # 3 Universes per roll
#     number_of_universes += (3 ** rolls) * ways_to_make_chain

# print(f"number of universes: {number_of_universes}")

max_ways_to_make_a_chain = max(ways_to_make_chain(c) for c in all_chains)
print(f"max ways to make a chain: {max_ways_to_make_a_chain}")

ways_to_make_all_chains = sum(ways_to_make_chain(c) for c in all_chains)
print(f"ways to make all chains: {ways_to_make_all_chains}")

shortest_chain = min(all_chains, key=lambda c: len(c.positions))
print(f"shortest chain ({len(shortest_chain.positions)}):\n{pformat(shortest_chain)}")

longest_chain = max(all_chains, key=lambda c: len(c.positions))
print(f"longest chain ({len(longest_chain.positions)}):\n{pformat(longest_chain)}")

# 444_356_092_776_315
# 341_960_390_180_808
# -------------------
# 786_316_482_957_123
# -------------------
# 1_657_838_170_544_193

# number of chains: 3847
# max ways to make a chain: 74088
# ways to make all chains: 5774185
