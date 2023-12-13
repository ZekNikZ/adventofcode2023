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
LEFT = 3
RIGHT = 1
UP = 0
DOWN = 2
LEFT2 = '-FL'
RIGHT2 = '-7J'
UP2 = '|7F'
DOWN2 = '|LJ'
ALLOWED_SYMBOLS_BY_DIRECTION = [UP2, RIGHT2, DOWN2, LEFT2]
ALLOWED_SYMBOLS = {
    '|': (True, False, True, False),
    '-': (False, True, False, True),
    'L': (True, True, False, False),
    'J': (True, False, False, True),
    'F': (False, True, True, False),
    '7': (False, False, True, True),
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

    # Figure out what symbol S actually is
    start_paths = tuple(in_grid((start_pos[0] + sdr, start_pos[1] + sdc)) and num_grid[start_pos[0] + sdr][start_pos[1] + sdc] > 0 and grid[start_pos[0] + sdr][start_pos[1] + sdc] in ALLOWED_SYMBOLS_BY_DIRECTION[i] for i, (sdr, sdc) in enumerate(DIRECTIONS))
    start_symbol = list(ALLOWED_SYMBOLS.keys())[list(ALLOWED_SYMBOLS.values()).index(start_paths)]
    print(f'Start symbol is {start_symbol}')

    if start_symbol == 'F':
        current = (start_pos[0], start_pos[1] + 1)
        fill_dir = DOWN
    elif start_symbol == '7':
        current = (start_pos[0], start_pos[1] - 1)
        fill_dir = DOWN
    elif start_symbol == 'L':
        current = (start_pos[0], start_pos[1] + 1)
        fill_dir = UP
    elif start_symbol == 'J':
        current = (start_pos[0], start_pos[1] - 1)
        fill_dir = UP
    elif start_symbol == '|':
        current = (start_pos[0] - 1, start_pos[1])
        while grid[current[0]][current[1]] == '|':
            current = (current[0] - 1, current[1])
        fill_dir = RIGHT if grid[current[0]][current[1]] == 'L' else LEFT
        current = (start_pos[0] - 1, start_pos[1])
    elif start_symbol == '-':
        current = (start_pos[0], start_pos[1] + 1)
        while grid[current[0]][current[1]] == '-':
            current = (current[0], current[1] + 1)
        fill_dir = UP if grid[current[0]][current[1]] == 'J' else DOWN
        current = (start_pos[0], start_pos[1] + 1)
    else:
        print("UH OH")
    fill_dir = (fill_dir + 2 )% 4

    num_grid[start_pos[0]][start_pos[1]] = 100
    num_insides = 0
    while in_grid(current) and current != start_pos and 0 <= num_grid[current[0]][current[1]] < 100:
        num_grid[current[0]][current[1]] += 100

        # Look for insides
        if grid[current[0]][current[1]] in '-|':
            start_inside = (current[0] + DIRECTIONS[fill_dir][0], current[1] + DIRECTIONS[fill_dir][1])
            if in_grid(start_inside) and num_grid[start_inside[0]][start_inside[1]] == -1:
                insides = [start_inside]
                while len(insides) > 0:
                    dot_current = insides.pop(0)
                    num_insides += 1
                    num_grid[dot_current[0]][dot_current[1]] = -2
                    for i, (dr, dc) in enumerate(DIRECTIONS):
                        potential = (current[0] + dr, current[1] + dc)
                        if in_grid(potential) and num_grid[start_inside[0]][start_inside[1]] == -1:
                            insides.append(potential)
        else:
            sym = grid[current[0]][current[1]]
            if sym == 'L':
                if fill_dir == UP:
                    fill_dir = RIGHT
                elif fill_dir == DOWN:
                    fill_dir = LEFT
                elif fill_dir == LEFT:
                    fill_dir = DOWN
                elif fill_dir == RIGHT:
                    fill_dir = UP
            elif sym == 'J':
                if fill_dir == UP:
                    fill_dir = LEFT
                elif fill_dir == DOWN:
                    fill_dir = RIGHT
                elif fill_dir == RIGHT:
                    fill_dir = DOWN
                elif fill_dir == LEFT:
                    fill_dir = UP
            elif sym == '7':
                if fill_dir == UP:
                    fill_dir = RIGHT
                elif fill_dir == DOWN:
                    fill_dir = LEFT
                elif fill_dir == LEFT:
                    fill_dir = DOWN
                elif fill_dir == RIGHT:
                    fill_dir = UP
            elif sym == 'F':
                if fill_dir == UP:
                    fill_dir = LEFT
                elif fill_dir == DOWN:
                    fill_dir = RIGHT
                elif fill_dir == RIGHT:
                    fill_dir = DOWN
                elif fill_dir == LEFT:
                    fill_dir = UP
            else:
                print('UH OH')

        # Go to next grid cell
        for i, dir in enumerate(DIRECTIONS):
            dr, dc = dir
            potential = (current[0] + dr, current[1] + dc)
            if in_grid(potential) and ALLOWED_SYMBOLS[grid[current[0]][current[1]]][i] and ((0 <= num_grid[potential[0]][potential[1]] < 100) or (n > 1 and 0 <= num_grid[potential[0]][potential[1]] <= 100)):
                current = potential
                break

    print(f"Result:", num_insides)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            print(grid[r][c] if num_grid[r][c] >= 100 else ('O' if num_grid[r][c] == -1 else 'I'), end='')
        print()
    break