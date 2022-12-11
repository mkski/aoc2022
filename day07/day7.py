inputs = open("in").read()


PROMPT = "$ "


class Directory:

    def __init__(self, name, parent=None):
        self.directories = {}
        self.files = []
        self.name = name
        self.parent = parent
        self.size_total = 0

    def add_dir(self, directory):
        if directory.name not in self.directories:
            self.directories[directory.name] = directory

    def add_file(self, f):
        self.files.append(f)

    @property
    def size(self):
        return sum([f.size for f in self.files]) + sum([d.size for d in self.directories.values()])

    def __str__(self):
        return f"<Directory {self.name}>"

    def __repr__(self):
        return self.__str__()


class File:

    def __init__(self, name, size):
        self.name = name
        self.size = size


def sum_sizes(d):
    def _sum_child(c):
        child_sizes = 0

        for child in c.directories.values():
            child_size = _sum_child(child)
            child_sizes += child_size

        this_size = child_sizes + c.size
        if this_size <= 100000:
            d.size_total += this_size
        return this_size
    _sum_child(d)
    return d.size_total


s = 0
directories = {}
root = current_dir = Directory("/")
for line in inputs.split("\n"):
    if line.startswith(PROMPT):
        cmd = line.strip(PROMPT)
        if cmd.startswith("cd"):
            cmd, arg = cmd.split()
            if arg == "..":
                current_dir = current_dir.parent
            elif arg == "/":
                current_dir = root
            else:
                current_dir = current_dir.directories[arg]
        elif cmd == "ls":
            continue
    elif line.startswith("dir"):
        _, dirname = line.split()
        d = Directory(dirname, parent=current_dir)
        current_dir.add_dir(d)
        if dirname not in directories:
            directories[dirname] = d
    elif line == "break":
        breakpoint()
    else:
        size, filename = line.split()
        current_dir.add_file(File(filename, int(size)))
        s += int(size)

print(sum_sizes(root))

total = 70000000
used = root.size
available = total - used
required = 30000000
needed = required - available

candidates = []

for d in directories.values():
    if d.size >= needed:
        candidates.append(d.size)

print(min(candidates))
