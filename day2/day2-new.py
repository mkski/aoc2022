with open("input") as f:
    guide = f.read()

rounds = guide.split("\n")

WIN = 6
TIE = 3
LOSE = 0


class RPS:

    def __gt__(self, o):
        if isinstance(o, self.beats):
            return WIN
        elif isinstance(o, type(self)):
            return TIE
        else:
            return LOSE


class Rock(RPS):

    def __init__(self):
        self.score = 1
        self.beats = Scissors
        self.beat_by = Paper


class Paper(RPS):

    def __init__(self):
        self.score = 2
        self.beats = Rock
        self.beat_by = Scissors


class Scissors(RPS):

    def __init__(self):
        self.score = 3
        self.beats = Paper
        self.beat_by = Rock


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
    