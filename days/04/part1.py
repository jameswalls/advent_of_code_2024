import pdb

def get_puzzle(path: str) -> list[list[str]]:
    lines = []
    with open(path, "r") as file:
        while line := file.readline():
            lines.append(list(line.strip()))

    return lines

def shifted_sub_puzzle(puzzle: list[list[str]], reverse=False):
    sub_puzzle = []

    for idx, item in enumerate(puzzle):
        if reverse:
            sub_puzzle.append(item[::-1][idx:])
        else:
            sub_puzzle.append(item[idx:])

    return list(zip(*sub_puzzle))

def scanner(puzzle: list[list[str]], size: int):
    n_rows = len(puzzle)
    n_cols = len(puzzle[0])

    for row in puzzle:
        for i in range(n_cols - size + 1):
            yield "".join(row[i:i+size])

    for col in zip(*puzzle):
        for i in range(n_rows - size + 1):
            yield "".join(col[i:i+size])

    for row_idx in range(n_rows - size + 1):
        sub_puzzle = shifted_sub_puzzle(puzzle[row_idx:row_idx+size])
        for item in sub_puzzle:
            yield "".join(item)

    for row_idx in range(n_rows - size + 1):
        sub_puzzle = shifted_sub_puzzle(puzzle[row_idx:row_idx+size], True)
        for item in sub_puzzle:
            yield "".join(item)
    
print(40*"-")
print("test")
puzzle = get_puzzle("./test.txt")
scan = iter(scanner(puzzle, 4))
matches = frozenset(["XMAS", "SAMX"])
total = sum(word in matches for word in scan)
print(f"total matches: {total}")

print(40*"-")
print("part 1")
puzzle = get_puzzle("./part1.txt")
scan = iter(scanner(puzzle, 4))
matches = frozenset(["XMAS", "SAMX"])
total = sum(word in matches for word in scan)
print(f"total matches: {total}")
