import sys

MAXIMUMS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

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

    for round in rounds:
        is_valid = True
        for color, amount in round.items():
            if amount > MAXIMUMS[color]:
                is_valid = False
                break

        if not is_valid:
            print('  => INVALID')
            break
    else:
        print('  => VALID')
        result += gameid


print(f"Result for {sys.argv[1]}:", result)