inputs = open("in").read().strip()
trees = [[int(c) for c in r] for r in inputs.split("\n")]

rows = len(trees)
cols = len(trees[0])

def check_n(row, col):
    for r in range(row-1, -1, -1):
        if trees[r][col] >= trees[row][col]:
            return False
    return True

def check_s(row, col):
    for r in range(row+1, rows):
        if trees[r][col] >= trees[row][col]:
            return False
    return True

def check_e(row, col):
    for c in range(col+1, cols):
        if trees[row][c] >= trees[row][col]:
            return False
    return True

def check_w(row, col):
    for c in range(col-1, -1, -1):
        if trees[row][c] >= trees[row][col]:
            return False
    return True

s = rows * 4 - 4
for r, tree_row in enumerate(trees[1:-1]):
    for c, tree_col in enumerate(tree_row[1:-1]):
        s += check_n(r+1, c+1) | check_s(r+1, c+1) | check_e(r+1, c+1) | check_w(r+1, c+1)
print(s)


def count_n(row, col):
    r = row - 1
    count = 0
    while r >= 0:
        if trees[r][col] < trees[row][col]:
            count += 1
        else:
            count += 1
            return count
        r -= 1
    return count

def count_s(row, col):
    r = row + 1
    count = 0
    while r < rows:
        if trees[r][col] < trees[row][col]:
            count += 1
        else:
            count += 1
            return count
        r += 1
    return count

def count_e(row, col):
    c = col + 1
    count = 0
    while c < cols:
        if trees[row][c] < trees[row][col]:
            count += 1
        else:
            count += 1
            return count
        c += 1
    return count

def count_w(row, col):
    c = col - 1
    count = 0
    while c >= 0:
        if trees[row][c] < trees[row][col]:
            count += 1
        else:
            count += 1
            return count
        c -= 1
    return count

scores = []
for r, tree_row in enumerate(trees):
    for c, tree_col in enumerate(tree_row):
        scores.append(count_n(r,c) * count_s(r,c) * count_e(r,c) * count_w(r,c))

print(max(scores))
