with open("input") as f:
    inputs = f.read()

elf_calories = inputs.split("\n\n")
elf_calories = [i.split("\n") for i in elf_calories]
elf_calories = [sum([int(j) for j in i]) for i in elf_calories]

# part 1
print(max(elf_calories))

# part 2
print(sum(sorted(elf_calories, reverse=True)[:3]))