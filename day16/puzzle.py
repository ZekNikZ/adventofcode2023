import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

grid = [line.strip() for line in sys.stdin]

def solve(starting_beam):
    global grid
    hot_grid = [[False] * len(row) for row in grid]

    # BEAM = (row, col, direction)
    beam_cache = set()
    beams = [starting_beam]
    while len(beams) > 0:
        beam = beams.pop(0)
        row, col, dir = beam

        # Discard if beam is not in grid
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
            continue

        # Discard if we have seen this beam before
        if beam in beam_cache:
            continue

        # Compute new beam(s)
        char = grid[row][col]
        if char == '.':
            if dir == NORTH:
                beams.append((row - 1, col, NORTH))
            elif dir == EAST:
                beams.append((row, col + 1, EAST))
            elif dir == SOUTH:
                beams.append((row + 1, col, SOUTH))
            elif dir == WEST:
                beams.append((row, col - 1, WEST))
        elif char == '/':
            if dir == NORTH:
                beams.append((row, col + 1, EAST))
            elif dir == EAST:
                beams.append((row - 1, col, NORTH))
            elif dir == SOUTH:
                beams.append((row, col - 1, WEST))
            elif dir == WEST:
                beams.append((row + 1, col, SOUTH))
        elif char == '\\':
            if dir == NORTH:
                beams.append((row, col - 1, WEST))
            elif dir == EAST:
                beams.append((row + 1, col, SOUTH))
            elif dir == SOUTH:
                beams.append((row, col + 1, EAST))
            elif dir == WEST:
                beams.append((row - 1, col, NORTH))
        elif char == '|':
            if dir == EAST or dir == WEST:
                beams.append((row - 1, col, NORTH))
                beams.append((row + 1, col, SOUTH))
            elif dir == NORTH:
                beams.append((row - 1, col, NORTH))
            elif dir == SOUTH:
                beams.append((row + 1, col, SOUTH))
        elif char == '-':
            if dir == NORTH or dir == SOUTH:
                beams.append((row, col + 1, EAST))
                beams.append((row, col - 1, WEST))
            elif dir == EAST:
                beams.append((row, col + 1, EAST))
            elif dir == WEST:
                beams.append((row, col - 1, WEST))

        # Mark the location as hot
        hot_grid[row][col] = True

        # Cache the beam
        beam_cache.add(beam)

    return sum(sum(1 if col else 0 for col in row) for row in hot_grid)

beams = []
beams += [(i, 0, EAST) for i in range(len(grid))]
beams += [(i, len(grid[0]) - 1, WEST) for i in range(len(grid))]
beams += [(0, i, SOUTH) for i in range(len(grid[0]))]
beams += [(len(grid) - 1, i, NORTH) for i in range(len(grid[0]))]
result = max(solve(b) for b in beams)

print(f"Part 1:", solve((0, 0, EAST)))
print(f"Part 2:", result)