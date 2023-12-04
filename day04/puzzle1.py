import sys
from collections import defaultdict
import re

def parse(lines):
    res = []

    i = 1
    for line in lines:
        parts = list(map(lambda l: set(map(int, l.split())), re.split(r'[:|]', line)[1:]))
        res.append((i, *parts))
        i += 1

    return res

with open(sys.argv[1]) as f:
    lines = [line.strip() for line in f.readlines()]

# Parse grid
lines = parse(lines)
print(lines)

# Find valid nums
result = 0
for card_id, winning_numbers, my_numbers in lines:
    intersect = my_numbers.intersection(winning_numbers)
    val = 0 if len(intersect) == 0 else 2 ** (len(intersect) - 1)
    print(f'Card id {card_id} has value {val}')
    result += val

print(f"Result for {sys.argv[1]}:", result)