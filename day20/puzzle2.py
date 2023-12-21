import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread
from queue import PriorityQueue
from copy import deepcopy
import functools

NORMAL = 0
FLIP_FLOP = 1
CONJUNCTION = 2
OUTPUT = 3
TRACKED_NODES = ['mp', 'qt', 'qb', 'ng']

graph = defaultdict(list)
reverse_graph = defaultdict(list)
initial_state = defaultdict(lambda: (NORMAL, None))

for line in sys.stdin:
    name, outputs = line.strip().split(' -> ')
    outputs = outputs.split(', ')
    if name == 'broadcaster':
        graph['broadcaster'] = outputs
    else:
        op, name = name[0], name[1:]
        graph[name] = outputs
        if op == '%':
            initial_state[name] = (FLIP_FLOP, 0)
        else:
            initial_state[name] = (CONJUNCTION, {})
    for out in outputs:
        reverse_graph[out].append(name)

for key, val in initial_state.items():
    if val[0] == CONJUNCTION:
        initial_state[key] = (CONJUNCTION, {name: 0 for name in reverse_graph[key]})

if 'rx' in graph:
    initial_state['rx'] = (OUTPUT, None)


# print(graph)
# print(reverse_graph)
# print(initial_state)

cache = {}

def compute_step(state):
    global graph

    hash = frozenset((s[0], (CONJUNCTION, frozenset(s[1][1]))) if s[1][0] == CONJUNCTION else s for s in state.items())
    if hash in cache:
        return cache[hash]

    new_state = deepcopy(state)

    low_pulses = 0
    high_pulses = 0
    tracked_hits = []

    pulses = [('button', 'broadcaster', 0)]

    while len(pulses) > 0:
        pulse = pulses.pop(0)
        source_node, target_node, pulse_strength = pulse
        if pulse_strength == 0:
            low_pulses += 1
        else:
            high_pulses += 1

        node_outputs = graph[target_node]
        node_type, node_state = new_state[target_node]
        if node_type == NORMAL:
            for output in node_outputs:
                pulses.append((target_node, output, 0))
        elif node_type == FLIP_FLOP:
            if pulse_strength == 0:
                node_state = 1 - node_state
                new_state[target_node] = (node_type, node_state)
                for output in node_outputs:
                    pulses.append((target_node, output, node_state))
        elif node_type == CONJUNCTION:
            node_state[source_node] = pulse_strength
            new_state[target_node] = (node_type, node_state)
            for output in node_outputs:
                pulses.append((target_node, output, 1 - prod(node_state.values())))

        if source_node in TRACKED_NODES and pulse_strength == 1:
            tracked_hits.append(source_node)

    res = low_pulses, high_pulses, new_state, tracked_hits
    cache[hash] = res
    return res

low_pulses, high_pulses = 0, 0
s = initial_state
indices = [None] * 4
for i in range(5000):
    l, h, s, tracked = compute_step(s)
    low_pulses += l
    high_pulses += h
    if tracked:
        for t in tracked:
            indices[TRACKED_NODES.index(t)] = i + 1
print(f"Part 2:", prod(indices))
