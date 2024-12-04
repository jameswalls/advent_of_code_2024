import pdb
import re

def load(path: str) -> list[str]:
    with open(path, "r") as file:
        lines = file.readlines()

    return lines

def mul(a, b):
    return a * b

def compute_toggled_total(lines: list[str]) -> int:
    pattern = r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))"
    total = 0
    enabled = True
    
    for line in lines:
        matches = re.findall(pattern, line)
        for match in matches:
            if match == "do()":
                enabled = True
                continue
            elif match == "don't()":
                enabled = False
                continue
            else:
                if enabled:
                    total += eval(match)

    return total

print(40*"-")
print("test")
lines = load("./test2.txt")
total = compute_toggled_total(lines)
print(f"total: {total}")

print(40*"-")
print("part 2")
lines = load("./part1.txt")
total = compute_toggled_total(lines)
print(f"total: {total}")
