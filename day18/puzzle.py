import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread
from queue import PriorityQueue

instructions = [tuple(line.strip().replace('(', '').replace(')', '').split()) for line in sys.stdin]
instructions = [(a, int(b), c) for a, b, c in instructions]

def part1():
    global instructions
    result = 1 # for starting square

    current_height = 0
    for direction, length, color in instructions:
        if direction == 'R':
            result += (current_height + 1) * length # include the line itself
        elif direction == 'L':
            result -= current_height * length # don't include the line
        elif direction == 'U':
            result += length # account for one of the edges
            current_height += length
        elif direction == 'D':
            current_height -= length

    return abs(result)

def parse(color):
    return 'RDLU'[int(color[-1])], eval(f'0x{color[1:-1]}')

def part2():
    global instructions
    result = 1 # for starting square

    current_height = 0
    for direction, length, color in instructions:
        direction, length = parse(color)
        if direction == 'R':
            result += (current_height + 1) * length # include the line itself
        elif direction == 'L':
            result -= current_height * length # don't include the line
        elif direction == 'U':
            result += length # account for one of the edges
            current_height += length
        elif direction == 'D':
            current_height -= length

    return abs(result)

print(f"Part 1:", part1())
print(f"Part 2:", part2())
