from collections import defaultdict
import pdb

def load(path: str) -> tuple[defaultdict, list[list]]:
    with open(path, "r") as file:
        rules = defaultdict(lambda: set())
        updates = []
        while line := file.readline():
            if line == "\n":
                break
            key, val = line.split("|")
            rules[int(key)].add(int(val))

        while line := file.readline():
            updates.append([int(i) for i in line.split(",")])

    return rules, updates

def sum_middle_valid_pages(rules: defaultdict, updates: list[list]) -> tuple[int, list[list]]:
    middle_pages = []
    invalid = []
    for update in updates:
        valid = True
        seen_pages = set()
        for page in update:
            if seen_pages.intersection(rules[page]):
                valid = False
                invalid.append(update)
                break
            seen_pages.add(page)

        if valid:
            middle_pages.append(update[len(update) // 2])

    return sum(middle_pages), invalid

def sum_middle_fixed_pages(rules: defaultdict, updates: list[list]) -> int:
    fixed_updates = []
    for update in updates:
        seen_pages = []
        for page in update:
            if rule_pages := rules[page].intersection(seen_pages):
                insert_idx = min(seen_pages.index(page) for page in rule_pages)
                seen_pages.insert(insert_idx, page)
            else:
                seen_pages.append(page)
        fixed_updates.append(seen_pages)

    return sum(update[len(update)//2] for update in fixed_updates)

print(40*"-")
print("test")
rules, updates = load("./test.txt")
total, invalid = sum_middle_valid_pages(rules, updates)
total_fixed = sum_middle_fixed_pages(rules, invalid)
print(f"total: {total}")
print(f"total fixed: {total_fixed}")

print(40*"-")
print("part 1")
rules, updates = load("./input.txt")
total, invalid = sum_middle_valid_pages(rules, updates)
total_fixed = sum_middle_fixed_pages(rules, invalid)
print(f"total: {total}")
print(f"total fixed: {total_fixed}")
