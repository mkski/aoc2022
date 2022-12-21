from ast import literal_eval

pairs = open("in").read().split("\n\n")


def retry(left, right):
    print(f"retrying {left} {right}")
    if isinstance(left, list) and len(left) == 0:
        return True
    elif isinstance(right, list) and len(right) == 0:
        return False

    if isinstance(left, list):
        return retry(left[0], right)
    elif isinstance(right, list):
        return retry(left, right[0])
    else:
        return left <= right

def compare(left, right):
    stop = min(len(left), len(right))
    print(f"comparing {left} {right}")
    for i in range(stop):
        l, r = left[i], right[i]
        if isinstance(l, int) and isinstance(r, int):
            print(f"comparing int {l} {r}")
            if l < r:
                return True
            elif l == r:
                continue
            else:
                return False
        
        elif isinstance(l, list) and isinstance(r, list):
            print(f"comparing list {l} {r}")
            if len(l) == 0:
                return True
            elif len(r) == 0:
                return False
            else:
                return len(l) >= stop and compare(l, r)

        elif isinstance(l, int):
            return compare([l], r)
        elif isinstance(r, int):
            return compare(l, [r])

    return len(left) <= len(right)


s = 0
for n, pair in enumerate(pairs, 1):
    print()
    left, right = [literal_eval(p) for p in pair.split("\n")]
    in_order = compare(left, right)
    print(n, in_order)
    s += n if in_order else 0
print(s)
    
    