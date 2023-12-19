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

strings = input().split(',')

result = sum(hash_string(s) for s in strings)

print(f"Result:", result)