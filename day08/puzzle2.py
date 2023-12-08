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
steps = 0
while any(not current.endswith('Z') for current in currents):
    for i, current in enumerate(currents):
        currents[i] = graph[current][directions[steps % len(directions)]]
    steps += 1

print(f"Result:", steps)