import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter

grid = [list(line.strip()) for line in sys.stdin]

def in_grid(pos):
    global grid
    r, c = pos
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])

start_pos = None
for row, line in enumerate(grid):
    try:
        col = line.index('S')
        start_pos = (row, col)
        break
    except:
        pass

# UP, RIGHT, DOWN, LEFT
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
LEFT = '-FL'
RIGHT = '-7J',
UP = '|7F'
DOWN = '|LJ'
ALLOWED_SYMBOLS_BY_DIRECTION = [UP, RIGHT, DOWN, LEFT]
ALLOWED_SYMBOLS = {
    '|': [True, False, True, False],
    '-': [False, True, False, True],
    'L': [True, True, False, False],
    'J': [True, False, False, True],
    'F': [False, True, True, False],
    '7': [False, False, True, True],
}

for i, dir in enumerate(DIRECTIONS):
    sdr, sdc = dir
    current = (start_pos[0] + sdr, start_pos[1] + sdc)
    if not in_grid(current) or grid[current[0]][current[1]] == '.' or not ALLOWED_SYMBOLS[grid[current[0]][current[1]]][(i + 2) % 4]:
        continue

    num_grid = [[-1] * len(grid[0]) for _ in range(len(grid))]
    n = 0
    num_grid[start_pos[0]][start_pos[1]] = 0
    while in_grid(current) and current != start_pos and num_grid[current[0]][current[1]] == -1:
        n += 1
        num_grid[current[0]][current[1]] = n
        for i, dir in enumerate(DIRECTIONS):
            dr, dc = dir
            potential = (current[0] + dr, current[1] + dc)
            if in_grid(potential) and ALLOWED_SYMBOLS[grid[current[0]][current[1]]][i] and ((num_grid[potential[0]][potential[1]] < 0) or (n > 1 and num_grid[potential[0]][potential[1]] <= 0)):
                current = potential
                break

    if current != start_pos:
        break

    print(f"Result:", n // 2 + 1)
    break