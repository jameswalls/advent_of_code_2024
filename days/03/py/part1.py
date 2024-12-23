import re

def load(path: str) -> list[str]:
    with open(path, "r") as file:
        lines = file.readlines()

    return lines

def mul(a, b):
    return a * b

def compute_total(lines: list[str]) -> int:
    pattern = r"(mul\(\d{1,3},\d{1,3}\))"
    total = 0
    for line in lines:
        total += sum(eval(s) for s in re.findall(pattern, line))
    
    return total

def compute_toggled_total(lines: list[str]) -> int:
    pattern = r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))"
    total = 0
    enabled = True
    
    for line in lines:
        matches = re.findall(pattern, line)
        for match in matches:
            if line == "do()":
                enabled = True
            elif line == "don't()":
                enabled = False
            else:
                if enabled:
                    total += eval(match)

    return total


print(40*"-")
print("test")
lines = load("./test.txt")
total = compute_total(lines)
print(f"total: {total}")

print(40*"-")
print("part 1")
lines = load("./part1.txt")
total = compute_total(lines)
print(f"total: {total}")


print(40*"-")
print("part 2")
lines = load("./part2.txt")
total = compute_total(lines)
print(f"total: {total}")
