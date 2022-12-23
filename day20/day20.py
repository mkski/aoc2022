from copy import deepcopy


class Number:

    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n)
    
    def __repr__(self):
        return self.__str__()


def mix(key, count):
    inputs = [Number(int(n) * key) for n in open("in")]
    l = len(inputs)

    updated = inputs.copy()
    for _ in range(count):
        for n in inputs:
            if n == 0:
                continue

            old_ind = updated.index(n)
            updated.pop(old_ind)
            new_ind = (n.n + old_ind) % (l-1)
            updated = updated[:new_ind] + [n] + updated[new_ind:]

    zero = [n for n in updated if n.n == 0][0]
    zero_ind = updated.index(zero)
    return updated[(zero_ind+1000)%l].n + updated[(zero_ind+2000)%l].n + updated[(zero_ind+3000)%l].n


print(mix(1, 1,))
print(mix(811589153, 10))
