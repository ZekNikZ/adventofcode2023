import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter

RANKS = 'AKQT98765432J'

def get_rank_strength(rank):
    return RANKS.index(rank)

def get_hand_strength(hand):
    sorted_hand = sorted(hand)
    symbols = Counter(sorted_hand)
    num_symbols = len(symbols)

    # Five of a kind
    if num_symbols == 1:
        return 0

    # Four of a kind
    if num_symbols == 2 and all(n == 1 or n == 4 for n in symbols.values()):
        return 1

    # Full house
    if num_symbols == 2 and all(n == 2 or n == 3 for n in symbols.values()):
        return 2

    # Three of a kind
    if num_symbols == 3 and any(n == 3 for n in symbols.values()):
        return 3

    # Two pair
    if num_symbols == 3 and any(n == 2 for n in symbols.values()):
        return 4

    # Single pair
    if num_symbols == 4:
        return 5

    # Trash
    return 6

def get_hand_key2(subhand, hand):
    return (get_hand_strength(subhand), *map(get_rank_strength, hand))

def get_hand_key(hand: str):
    non_joker_symbols = set(hand) - {'J'}

    # Edge case
    if len(non_joker_symbols) == 0:
        non_joker_symbols = {'K'}

    subhands = []
    for replacements in itertools.combinations_with_replacement(non_joker_symbols, hand.count('J')):
        subhand = list(hand)
        j = 0
        for i, c in enumerate(subhand):
            if c == 'J':
                subhand[i] = replacements[j]
                j += 1
        subhands.append(get_hand_key2(''.join(subhand), hand))

    return min(subhands)

hands = [(hand, int(value), get_hand_key(hand)) for hand, value in (line.strip().split() for line in sys.stdin)]

result = sum(value * (i + 1) for i, (hand, value, key) in enumerate(sorted(hands, key=itemgetter(2), reverse=True)))

print(f"Result:", result)