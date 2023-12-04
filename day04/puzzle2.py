import sys
from collections import defaultdict
import re

def parse(lines):
    res = []

    i = 0
    for line in lines:
        parts = list(map(lambda l: set(map(int, l.split())), re.split(r'[:|]', line)[1:]))
        res.append((i, *parts))
        i += 1

    return res

lines = [line.strip() for line in sys.stdin.readlines()]
num_lines = len(lines)

# Parse grid
lines = parse(lines)

# Find valid nums
result = 0
card_counts = [1 for line in lines]
num_matches = [
    len(my_numbers.intersection(winning_numbers)) for _, winning_numbers, my_numbers in lines
]

for card_id, _, _ in lines:
    print(f'Card {card_id} has {card_counts[card_id]} copies with {num_matches[card_id]} matches')
    for i in range(card_id + 1, min(num_lines, card_id + num_matches[card_id] + 1)):
        card_counts[i] += card_counts[card_id]
        print(f'  Adding {card_counts[card_id]} copies of card {i}')

result = sum(card_counts[i] for i in range(num_lines))

print(f"Result:", result)