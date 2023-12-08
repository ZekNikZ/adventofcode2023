import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter

directions = [0 if x == 'L' else 1 for x in input()]
input()

graph = {}
for line in sys.stdin:
    start, left, right = filter(lambda x: x, re.split(r'[^a-zA-Z0-9]', line.strip()))
    graph[start] = (left, right)

currents = list(filter(lambda x: x.endswith('A'), graph.keys()))
steps = []
for i, c in enumerate(currents):
    current = c
    step = 0
    while not current.endswith('Z'):
        current = graph[current][directions[step % len(directions)]]
        step += 1
    steps.append(step)

print(f"Result:", lcm(*steps))