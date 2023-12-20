import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread
from queue import PriorityQueue

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

grid = [list(map(int, list(line.strip()))) for line in sys.stdin]

def is_in_grid(row, col):
    global grid
    return not (row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]))

def solve(start_pos, end_pos, min_before_turning, max_before_turning):
    global grid
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    state_cache = set()

    # dist_so_far, row, col, last_moved_direction, steps_in_last_direction
    pq = PriorityQueue()
    pq.put((0, start_row, start_col, WEST, 0))
    pq.put((0, start_row, start_col, NORTH, 0))
    pq.put((0, start_row, start_col, SOUTH, 0))
    pq.put((0, start_row, start_col, EAST, 0))

    while not pq.empty():
        pos = pq.get()
        dist, row, col, dir, steps = pos

        if row == end_row and col == end_col and steps >= min_before_turning:
            return dist

        # Discard if beam is not in grid
        if not is_in_grid(row, col):
            continue

        # Discard if we have seen this state before
        if pos[1:] in state_cache:
            continue

        if dir != SOUTH and ((dir != NORTH and steps >= min_before_turning) or (dir == NORTH and steps < max_before_turning)) and is_in_grid(row - 1, col):
            pq.put((dist + grid[row - 1][col], row - 1, col, NORTH, 1 if dir != NORTH else steps + 1))
        if dir != NORTH and ((dir != SOUTH and steps >= min_before_turning) or (dir == SOUTH and steps < max_before_turning)) and is_in_grid(row + 1, col):
            pq.put((dist + grid[row + 1][col], row + 1, col, SOUTH, 1 if dir != SOUTH else steps + 1))
        if dir != EAST and ((dir != WEST and steps >= min_before_turning) or (dir == WEST and steps < max_before_turning)) and is_in_grid(row, col + 1):
            pq.put((dist + grid[row][col + 1], row, col + 1, WEST, 1 if dir != WEST else steps + 1))
        if dir != WEST and ((dir != EAST and steps >= min_before_turning) or (dir == EAST and steps < max_before_turning)) and is_in_grid(row, col - 1):
            pq.put((dist + grid[row][col - 1], row, col - 1, EAST, 1 if dir != EAST else steps + 1))

        # Cache the beam
        state_cache.add(pos[1:])

print(f"Part 1:", solve((0, 0), (len(grid) - 1, len(grid[0]) - 1), 0, 3))
print(f"Part 2:", solve((0, 0), (len(grid) - 1, len(grid[0]) - 1), 4, 10))
