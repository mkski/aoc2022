inputs = open("in").read().split("\n")

def parse_cmd_lines(lines):
    dir_sizes = {"/": 0}
    for line in lines:
        match line.split():
            case "$", "cd", "/":
                current_path = ["/"]
            case "$", "cd", "..":
                current_path.pop()
            case "$", "cd", directory:
                current_path.append(directory)
            case "dir", directory:
                continue
            case "$", "ls":
                continue
            case size, _:
                p = ""
                for d in current_path:
                    p += d
                    if p in dir_sizes:
                        dir_sizes[p] += int(size)
                    else:
                        dir_sizes[p] = int(size)
    return dir_sizes


dir_sizes = parse_cmd_lines(inputs)
print(sum(s for s in dir_sizes.values() if s <= 100000))

needed = 30000000 - (70000000 - dir_sizes["/"])
candidates = [d for d in dir_sizes.values() if d >= needed]
print(min(candidates))
