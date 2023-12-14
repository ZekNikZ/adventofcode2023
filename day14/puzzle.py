import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from copy import deepcopy

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

starting_grid = [list(line.strip()) for line in sys.stdin]

def grid_hash(grid):
    return tuple(tuple(row) for row in grid)

def move_in_direction(grid, direction: int):
    grid = deepcopy(grid)

    if direction == NORTH:
        for c in range(len(grid[0])):
            for r in range(1, len(grid)):
                if grid[r][c] == 'O' and grid[r - 1][c] == '.':
                    rr = r - 1
                    while rr >= 0 and grid[rr][c] == '.':
                        rr -= 1
                    grid[r][c], grid[rr + 1][c] = grid[rr + 1][c], grid[r][c]
    elif direction == SOUTH:
        for c in range(len(grid[0])):
            for r in range(len(grid) - 2, -1, -1):
                if grid[r][c] == 'O' and grid[r + 1][c] == '.':
                    rr = r + 1
                    while rr < len(grid) and grid[rr][c] == '.':
                        rr += 1
                    grid[r][c], grid[rr - 1][c] = grid[rr - 1][c], grid[r][c]
    elif direction == WEST:
        for r in range(len(grid)):
            for c in range(1, len(grid[0])):
                if grid[r][c] == 'O' and grid[r][c - 1] == '.':
                    cc = c - 1
                    while cc >= 0 and grid[r][cc] == '.':
                        cc -= 1
                    grid[r][c], grid[r][cc + 1] = grid[r][cc + 1], grid[r][c]
    elif direction == EAST:
        for r in range(len(grid)):
            for c in range(len(grid[0]) - 2, -1, -1):
                if grid[r][c] == 'O' and grid[r][c + 1] == '.':
                    cc = c + 1
                    while cc < len(grid[0]) and grid[r][cc] == '.':
                        cc += 1
                    grid[r][c], grid[r][cc - 1] = grid[r][cc - 1], grid[r][c]

    return grid

def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()

def compute_weight(grid):
    return sum(row.count('O') * (len(grid) - i) for i, row in enumerate(grid))


# Part 1
grid = move_in_direction(starting_grid, NORTH)
result1 = compute_weight(grid)
print(f"Result part 1:", result1)

# Part 2
directions = [NORTH, WEST, SOUTH, EAST]
CACHE = dict()
a = None
c = None
grid = starting_grid
for i in range(1000000000):
    h = grid_hash(grid)
    if h in CACHE:
        a = CACHE[h]
        c = i - CACHE[h]
        break
    else:
        CACHE[h] = i

    for d in directions:
        grid = move_in_direction(grid, d)

i = a + ((1000000000 - a) % c)
grid = list(CACHE.keys())[list(CACHE.values()).index(i)]

result2 = compute_weight(grid)
print(f"Result part 2:", result2)
