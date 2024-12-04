import pdb

def get_puzzle(path: str) -> list[list[str]]:
    lines = []
    with open(path, "r") as file:
        while line := file.readline():
            lines.append(list(line.strip()))

    return lines


def scanner(puzzle: list[list[str]]):
    n_rows = len(puzzle)
    n_cols = len(puzzle[0])

    for row in range(1, n_rows-1):
        for col in range(1, n_cols-1):
            item = puzzle[row][col]
            if item == "A":
                yield f"{puzzle[row-1][col-1]}{puzzle[row-1][col+1]}{puzzle[row+1][col-1]}{puzzle[row+1][col+1]}"
    
print(40*"-")
print("test")
puzzle = get_puzzle("./test2.txt")
scan = iter(scanner(puzzle))
# print([i for i in scan])
matches = frozenset({"MSMS","SMSM", "SSMM", "MMSS"})
total = sum(word in matches for word in scan)
print(f"total matches: {total}")

print(40*"-")
print("part2")
puzzle = get_puzzle("./part1.txt")
scan = iter(scanner(puzzle))
matches = frozenset({"MSMS","SMSM", "SSMM", "MMSS"})
total = sum(word in matches for word in scan)
print(f"total matches: {total}")

