import sys
from collections import defaultdict

def parse(s):
    sets = s.split(',')
    return {parts[1]: int(parts[0]) for parts in map(lambda s: s.strip().split(' '), sets)}

with open(sys.argv[1]) as f:
    games = [line.strip() for line in f.readlines()]

result = 0
for game in games:
    gameid, rounds = game.split(': ')
    gameid = int(gameid.split(' ')[1])
    rounds = list(map(parse, rounds.split('; ')))
    print(gameid, rounds)

    counts = defaultdict(list)

    for round in rounds:
        for color, amount in round.items():
            counts[color].append(amount)

    counts = { k: max(v) for k, v in counts.items() }

    power = counts['red'] * counts['blue'] * counts['green']
    print(f'  => POWER: {power}')
    result += power


print(f"Result for {sys.argv[1]}:", result)