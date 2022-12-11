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
        return self.files_size + sum([d.size for d in self.directories.values()])

    @property
    def files_size(self):
        return sum([f.size for f in self.files])

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

        this_size = child_sizes + c.files_size
        if this_size <= 100000:
            d.size_total += this_size
        return this_size
    _sum_child(d)
    return d.size_total


def parse_cmd_lines(lines):
    root =  Directory("/")
    directories = {}
    for line in lines:
        match line.split():
            case "$", "cd", "/":
                current = root
            case "$", "cd", "..":
                current = current.parent
            case "$", "cd", directory:
                current = current.directories[directory]
            case "$", "ls":
                continue
            case "dir", directory:
                directories[directory] = Directory(directory, parent=current)
                current.add_dir(directories[directory])
            case size, filename:
                current.add_file(File(filename, int(size)))
    return root, directories


root, directories = parse_cmd_lines(inputs.split("\n"))
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
