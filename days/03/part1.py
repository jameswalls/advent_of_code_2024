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
