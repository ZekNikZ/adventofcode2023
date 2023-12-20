import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread
from queue import PriorityQueue

workflows = {}
parts = []

def parse_instruction(instruction):
    n, r = instruction[2:].split(':')
    return instruction[0], instruction[1], int(n), r

for line in sys.stdin:
    line = line.strip()

    if line.startswith('{'):
        # Part
        parts.append(tuple(map(int, re.findall(r'\d+', line))))
    elif line:
        # Workflow
        name, instructions = line[:-1].split('{')
        *parsed_instructions, otherwise = instructions.split(',')
        workflows[name] = (list(map(parse_instruction, parsed_instructions)), otherwise)

stack = [('in', [(1, 4000), (1, 4000), (1, 4000), (1, 4000)])]
complete_ranges = []

while len(stack) > 0:
    s = stack.pop(0)
    current_workflow, current_ranges = s

    if current_workflow in 'AR':
        complete_ranges.append(s)
        continue

    instructions, otherwise = workflows[current_workflow]
    # print(s, instructions, otherwise)
    for var, op, n, res in instructions:
        affected_index = 'xmas'.index(var)
        affected_range = current_ranges[affected_index]
        if op == '<':
            if affected_range[0] >= n:
                continue
            correct_range = (affected_range[0], n - 1)
            incorrect_range = (n, affected_range[1])
            ranges = list(current_ranges)
            ranges[affected_index] = correct_range
            stack.append((res, ranges))
            # print(' ', stack[-1])
            current_ranges[affected_index] = incorrect_range
        else:
            if affected_range[1] <= n:
                continue
            incorrect_range = (affected_range[0], n)
            correct_range = (n + 1, affected_range[1])
            ranges = list(current_ranges)
            ranges[affected_index] = correct_range
            stack.append((res, ranges))
            # print(' ', stack[-1])
            current_ranges[affected_index] = incorrect_range

    stack.append((otherwise, current_ranges))
    # print(' ', stack[-1])

part1 = 0
for pieces in parts:
    for status, ranges in complete_ranges:
        if status == 'A':
            valid = True
            for i in range(4):
                if not (ranges[i][0] <= pieces[i] <= ranges[i][1]):
                    valid = False
            if valid:
                part1 += sum(pieces)

part2 = 0
for status, ranges in complete_ranges:
    res = 1
    if status == 'A':
        for a, b in ranges:
            res *= b - a + 1
        part2 += res


print(f"Part 1:", part1)
print(f"Part 2:", part2)
