import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter

x_list = []
y_list = []
x_expansions = []
y_expansions = []

grid = []

for x, line in enumerate(sys.stdin):
    line = line.strip()
    grid.append(line)
    for y, c in enumerate(line):
        if c == '#':
            x_list.append(x)
            y_list.append(y)
    if '#' not in line:
        x_expansions.append(x)

for y, col in enumerate(zip(*grid)):
    if '#' not in col:
        y_expansions.append(y)

x_list.sort()
y_list.sort()

total_distance = 0
expansion_coefficient = 0

# Total distance
total_distance = sum(b - a for a, b in itertools.combinations(x_list, 2)) + sum(b - a for a, b in itertools.combinations(y_list, 2))

# Expansion coefficient
for x_expansion in x_expansions:
    i = 0
    for x in x_list:
        if x_expansion < x:
            break
        i += 1
    expansion_coefficient += i * (len(x_list) - i)
for y_expansion in y_expansions:
    i = 0
    for y in y_list:
        if y_expansion < y:
            break
        i += 1
    expansion_coefficient += i * (len(y_list) - i)

print(f"Result part 1:", total_distance + expansion_coefficient)
print(f"Result part 2:", total_distance + 999999 * expansion_coefficient)