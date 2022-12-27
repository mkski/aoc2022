inputs = open("in")
test_inputs = open("in-test")


def parse_input(inputs):
    numbers = []
    for line in inputs:
        numbers.append(line.strip())
    return numbers


def snafu_to_dec(num):
    exp = len(num) - 1
    decimal = 0
    for char in num:
        try:
            decimal += int(char) * 5**exp
        except ValueError:
            decimal += (-2 if char == "=" else -1) * 5**exp
        exp -= 1
    return decimal


def dec_to_snafu(num):
    snafu = ""
    while num:
        num, rem = divmod(num, 5)
        if rem == 0:
            snafu = f"0{snafu}"
        elif rem < 3:
            snafu = f"{rem}{snafu}"
        elif rem == 3:
            snafu = f"={snafu}"
            num += 1
        elif rem == 4:
            snafu = f"-{snafu}"
            num += 1
    return snafu


def get_total(numbers):
    return sum(snafu_to_dec(n) for n in numbers)


numbers = parse_input(inputs)
print(dec_to_snafu(get_total(numbers)))
