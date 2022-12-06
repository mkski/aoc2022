signal = open("input").read()

def find_unique_window(signal, size):
    for n, _ in enumerate(signal[:-size]):
        window = signal[n:n+size]
        if len(set(window)) == size:
            return n + size

print(find_unique_window(signal, 4))
print(find_unique_window(signal, 14))
