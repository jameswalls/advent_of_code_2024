from collections import defaultdict

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

print(40*"-")
print("test")
rules, updates = load("./test.txt")
total = sum_middle_valid_pages(rules, updates)
print(f"total: {total}")


print(40*"-")
print("part 1")
rules, updates = load("./input.txt")
total = sum_middle_valid_pages(rules, updates)
print(f"total: {total}")
