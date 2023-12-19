import sys
from collections import defaultdict, Counter
import re
import itertools
from math import *
from operator import itemgetter
from threading import Thread

def hash_string(s):
    val = 0

    for c in s:
        val += ord(c)
        val *= 17
        val %= 256

    return val

boxes = [[] for _ in range(256)]

for s in input().split(','):
    label = re.split(r'[=-]', s)[0]
    box = hash_string(label)
    action = s[len(label)]
    try:
        i = [a for a, _ in boxes[box]].index(label)
    except:
        i = None
    if action == '-':
        if i is not None:
            boxes[box].pop(i)
    else:
        num = int(s[len(label) + 1])
        if i is not None:
            boxes[box][i] = (label, num)
        else:
            boxes[box].append((label, num))

result = 0
for i, box in enumerate(boxes):
    for j, (label, lens) in enumerate(box):
        result += (i + 1) * (j + 1) * lens

print(f"Result:", result)