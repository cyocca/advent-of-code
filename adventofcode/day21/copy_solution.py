from __future__ import annotations
from collections import defaultdict
from adventofcode.utils import load_list
from typing_extensions import Final
from itertools import chain, cycle, combinations_with_replacement, permutations, product, repeat
from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple
from pprint import pprint, pformat

@dataclass
class Player:

    pos: int
    score: int = 0
    winning_score: int = 1000

    @classmethod
    def parse(cls, line: str) -> Player:
        # The position is the last char on the line
        return cls(pos=int(line[-1]))

    @property
    def has_winning_score(self) -> bool:
        return self.winning_score <= self.score

    def move(self, spaces: int) -> None:
        self.pos = (self.pos + spaces) % SPACES
        # Make sure 10 stays 10 because the position is 1-indexed
        if self.pos == 0:
            self.pos = 10

        self.score += self.pos

SPACES: Final = 10

def get_players(winning_score: int) -> List[Player]:
    players = load_list(parser=Player.parse)
    for p in players:
        p.winning_score = winning_score
    return players

def play(die: Iterable[int], players: List[Player], rolls_per_turn: int) -> int:
    player_index = 0
    rolls = 0

    while all(not p.has_winning_score for p in players):
        # Roll the die three times and add up the moves
        spaces = sum(next(die) for _ in range(rolls_per_turn))
        rolls += rolls_per_turn

        players[player_index].move(spaces)
        # Go to the next player
        player_index = (player_index + 1) % len(players)

    return rolls

def part_1() -> int:
    # Repeat the numbers [1, 100]
    die = cycle(range(1, 101))
    players = get_players(winning_score=1000)

    rolls = play(die, players, rolls_per_turn=3)

    # Find the player without a winning score
    loser = next(p for p in players if not p.has_winning_score)
    return loser.score * rolls

print(part_1())

def part_2() -> int:
    # The die will give any combination of (1, 2, 3) for a turn
    pairs_of_die_rolls = combinations_with_replacement(range(1, 4), 3)
    # The number of possible spaces to move in a turn
    space_counts = {sum(p) for p in pairs_of_die_rolls}
    # Assume it won't take more than 11 turns for someone to win
    dice = combinations_with_replacement(space_counts, 11)

    wins = [0, 0]
    for die in dice:
        players = get_players(winning_score=21)
        play(iter(die), players, rolls_per_turn=1)
        winner_index = next(index for index, p in enumerate(players) if p.has_winning_score)
        wins[winner_index] += 1

    from pprint import pprint
    pprint(wins)

# part_2()
# players = get_players(winning_score=21)
# rolls = play(repeat(3), players)
# breakpoint()

# from pprint import pprint
# from itertools import combinations_with_replacement
# We need permutations with replacement, i.e. every order of every roll including 1, 2,
# and 3
pairs_of_die_rolls = list(product(range(1, 4), repeat=3))
spaces_moved_to_ways = defaultdict(int)
for pair in pairs_of_die_rolls:
    spaces_moved_to_ways[sum(pair)] += 1
pprint(spaces_moved_to_ways)
space_counts = {sum(p) for p in pairs_of_die_rolls}
# pprint(pairs_of_die_rolls)
# pprint(space_counts)
# print(len(list(combinations_with_replacement(space_counts, 10))))

# first = 444356092776315
# second = 341960390180808
# total = first + second
# print(first / total)
# print(second / total)

# space_to_predecessors = defaultdict(set)
# for space in range(1, 11):
#     for move in space_counts:
#         pos = (space + move) % SPACES
#         # Make sure 10 stays 10 because the position is 1-indexed
#         if pos == 0:
#             pos = 10

#         space_to_predecessors[pos].add(space)
# pprint(space_to_predecessors)

@dataclass
class Space:

    pos: int
    spaces_moved: int

# space_to_successors = defaultdict(set)
space_to_successors = defaultdict(list)
for space in range(1, 11):
    for move in space_counts:
        pos = (space + move) % SPACES
        # Make sure 10 stays 10 because the position is 1-indexed
        if pos == 0:
            pos = 10

        # space_to_successors[space].add(pos)
        space_to_successors[space].append(Space(pos, move))
# pprint(space_to_successors)

# def get_winning_chains(score: int, winning_score: int, cur_pos: int, cur_chain: List[int], chains: List[List[int]]) -> None:
#     score += cur_pos
#     cur_chain = [*cur_chain, cur_pos]

#     if score >= winning_score:
#         chains.append(cur_chain)
#         # chains.add(tuple(cur_chain))
#         return

#     for pos in space_to_successors[cur_pos]:
#         get_winning_chains(score, winning_score, pos, cur_chain, chains)

# def get_winning_chains(score: int, winning_score: int, cur_space: Space, cur_chain: List[int], chains: List[List[Space]]) -> None:
#     if cur_chain:
#         # Don't add to the score for the starting pos
#         score += cur_space.pos

#     cur_chain = [*cur_chain, cur_space]

#     if score >= winning_score:
#         chains.append(cur_chain)
#         return

#     for pos in space_to_successors[cur_space.pos]:
#         get_winning_chains(score, winning_score, pos, cur_chain, chains)

# chains = set()
# chains = []
# player_1_chains = []
# get_winning_chains(0, 21, Space(4, -1), [], player_1_chains)
# player_2_chains = []
# get_winning_chains(0, 21, Space(8, -1), [], player_2_chains)
# all_chains = [*player_1_chains, *player_2_chains]

@dataclass
class Chain:

    positions: List[int]
    score: int

    @property
    def cur_position(self) -> int:
        return self.positions[-1]

    def move(self, spaces: int) -> None:
        new_pos = (self.cur_pos + spaces) % SPACES

        # Make sure 10 stays 10 because the position is 1-indexed
        if new_pos == 0:
            new_pos = 10

        self.score += new_pos
        self.positions.append(new_pos)


def get_winning_chains(
    score1: int,
    score2: int,
    winning_score: int,
    cur_space1: Space,
    cur_space2: Space,
    cur_chain1: List[int],
    cur_chain2: List[int],
    chains: List[List[Space]],
    # Player 1 first
    turn: bool = True,
) -> None:
    if cur_chain1:
        # Don't add to the score for the starting pos
        if turn:
            score1 += cur_space1.pos
        else:
            score2 += cur_space2.pos

    if turn:
        cur_chain1 = [*cur_chain1, cur_space1]
    else:
        cur_chain2 = [*cur_chain2, cur_space2]

    if score1 >= winning_score:
        chains.append(cur_chain1)
        return

    if score2 >= winning_score:
        chains.append(cur_chain2)
        return

    def get_new_pos(pos, move):
        pos = (pos + move) % SPACES
        # Make sure 10 stays 10 because the position is 1-indexed
        if pos == 0:
            return 10

        return pos

    for move in space_counts:
        if turn:
            space2 = Space(get_new_pos(cur_space2.pos, move), move)
            get_winning_chains(score1, score2, winning_score, cur_space1, space2, cur_chain1, cur_chain2, chains, not turn)
        else:
            space1 = Space(get_new_pos(cur_space1.pos, move), move)
            get_winning_chains(score1, score2, winning_score, space1, cur_space2, cur_chain1, cur_chain2, chains, not turn)

all_chains = []
get_winning_chains(0, 0, 21, Space(4, -1), Space(8, -1), [], [], all_chains)

# use `spaces_moved_to_ways` to map each chain ^ to the number of ways that chain can occur.
# For example 1 -> 4 -> 9 -> ...
# you move 3 (1 possible way) then 5 (2 possible ways) so the number of ways to create
# that chain so far is 1 * 2 = 2
# When we find the total number of ways to make the chains, we can divide each players
# number of winning chains by the total number of chains

print(f"number of chains: {len(all_chains)}")

def ways_to_make_chain(chain):
    ways_to_make_chain = 1

    for moved in (space.spaces_moved for space in chain[1:]):
        ways_to_make_chain *= spaces_moved_to_ways[moved]

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

shortest_chain = min(all_chains, key=lambda c: len(c))
print(f"shortest chain ({len(shortest_chain)}):\n{pformat(shortest_chain)}")

longest_chain = max(all_chains, key=lambda c: len(c))
print(f"longest chain ({len(longest_chain)}):\n{pformat(longest_chain)}")

# 444_356_092_776_315
# 341_960_390_180_808
# -------------------
# 786_316_482_957_123
# -------------------
# 1_657_838_170_544_193

# number of chains: 3847
# max ways to make a chain: 74088
# ways to make all chains: 5774185
