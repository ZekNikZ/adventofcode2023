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
    grid[start_pos[0]][start_pos[1]] = start_symbol
    print(f'Start symbol is {start_symbol}')

    num_insides = 0
    for r in range(len(grid)):
        inside = False
        for c in range(len(grid[0])):
            if grid[r][c] == '|' and num_grid[r][c] >= 0:
                inside = not inside
                # print(f'row {r} col {c} now {inside} 1')
            elif c < len(grid[0]) - 1 and grid[r][c] in 'FL' and num_grid[r][c] >= 0:
                other = '7' if grid[r][c] == 'L' else 'J'
                # print(f'>row {r} col {c} checking 2 {other}')
                for c2 in range(c+1, len(grid[0])):
                    # print(f'  >checking row {r} col {c2} checking 2 {other}')
                    if num_grid[r][c2] < 0:
                        # print('  break')
                        break
                    elif grid[r][c2] == '-':
                        pass
                    elif grid[r][c2] == other:
                        inside = not inside
                        # print(f'row {r} col {c} now {inside} 2')
                        break
                    else:
                        break
            elif num_grid[r][c] == -1:
                if inside:
                    num_insides += 1
                    num_grid[r][c] = -3
                else:
                    num_grid[r][c] = -4

    # if start_symbol == 'F':
    #     current = (start_pos[0], start_pos[1] + 1)
    # elif start_symbol == '7':
    #     current = (start_pos[0], start_pos[1] - 1)
    # elif start_symbol == 'L':
    #     current = (start_pos[0], start_pos[1] + 1)
    # elif start_symbol == 'J':
    #     current = (start_pos[0], start_pos[1] - 1)
    # elif start_symbol == '|':
    #     current = (start_pos[0] - 1, start_pos[1])
    # elif start_symbol == '-':
    #     current = (start_pos[0], start_pos[1] + 1)
    # else:
    #     print("UH OH")

    # num_grid[start_pos[0]][start_pos[1]] = 100
    # num_insides = 0
    # while in_grid(current) and current != start_pos and 0 <= num_grid[current[0]][current[1]] < 100:
    #     num_grid[current[0]][current[1]] += 100

    #     # Look for insides
    #     for fill_dir in range(4):
    #         start_inside = (current[0] + DIRECTIONS[fill_dir][0], current[1] + DIRECTIONS[fill_dir][1])
    #         if in_grid(start_inside) and num_grid[start_inside[0]][start_inside[1]] == -1:
    #             visited = []
    #             valid = True
    #             insides = [start_inside]
    #             while len(insides) > 0:
    #                 if not valid:
    #                     break
    #                 dot_current = insides.pop(0)
    #                 if dot_current in visited:
    #                     continue
    #                 visited.append(dot_current)
    #                 num_grid[dot_current[0]][dot_current[1]] = -2
    #                 for i, (dr, dc) in enumerate(DIRECTIONS):
    #                     potential = (dot_current[0] + dr, dot_current[1] + dc)
    #                     if in_grid(potential) and num_grid[potential[0]][potential[1]] == -1:
    #                         insides.append(potential)
    #                     elif not in_grid(potential) or num_grid[potential[0]][potential[1]] == -4:
    #                         valid = False
    #                         break
    #             if valid:
    #                 num_insides += len(visited)
    #                 for r, c in visited:
    #                     num_grid[r][c] = -3
    #             else:
    #                 for r, c in visited:
    #                     num_grid[r][c] = -4

    #     # Go to next grid cell
    #     for i, dir in enumerate(DIRECTIONS):
    #         dr, dc = dir
    #         potential = (current[0] + dr, current[1] + dc)
    #         if in_grid(potential) and ALLOWED_SYMBOLS[grid[current[0]][current[1]]][i] and ((0 <= num_grid[potential[0]][potential[1]] < 100) or (n > 1 and 0 <= num_grid[potential[0]][potential[1]] <= 100)):
    #             current = potential
    #             break

    print(f"Result:", num_insides)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            print(grid[r][c] if num_grid[r][c] >= 0 else ('I' if num_grid[r][c] == -3 else ('O' if num_grid[r][c] == -4 else ('X' if num_grid[r][c] == -2 else 'Y'))), end='')
        print()
    break