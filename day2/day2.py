with open("in") as f:
    guide = f.read()

rounds = guide.split("\n")

WIN = 6
TIE = 3
LOSE = 0


class Paper:
    score = 2

    def __gt__(self, o):
        if isinstance(o, Rock):
            return WIN
        elif isinstance(o, Paper):
            return TIE
        else:
            return LOSE

class Scissors:
    score = 3

    def __gt__(self, o):
        if isinstance(o, Paper):
            return WIN
        elif isinstance(o, Scissors):
            return TIE
        else:
            return LOSE

class Rock:
    score = 1

    def __gt__(self, o):
        if isinstance(o, Scissors):
            return WIN
        elif isinstance(o, Rock):
            return TIE
        else:
            return LOSE

Rock.beat_by = Paper
Rock.beats = Scissors
Paper.beat_by = Scissors
Paper.beats = Rock
Scissors.beat_by = Rock
Scissors.beats = Paper

d = {
    "A": Rock,
    "B": Paper,
    "C": Scissors,
    "X": Rock,
    "Y": Paper,
    "Z": Scissors
}

score = 0

for r in rounds:
    opp, me = r.split()
    my_move = d[me]()
    opp_move = d[opp]()
    score += my_move.score + (my_move > opp_move)

print(score)

score = 0
for r in rounds:
    opp, out = r.split()
    opp_move = d[opp]()

    if out == "X":
        my_move = opp_move.beats()
    elif out == "Y":
        my_move = opp_move
    else:
        my_move = opp_move.beat_by()

    score += my_move.score + (my_move > opp_move)

print(score)
