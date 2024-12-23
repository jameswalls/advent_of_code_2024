import pdb
from collections import Counter

def read_lists(path: str) -> tuple[list, list]:
    left_list = []
    right_list = []
    with open(path, "r") as file:
        for line in file.readlines():
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))

    return left_list, right_list

def compute_similarity_score(left: list, right: list):
    right_counts = Counter(right)
    similarity_score = sum(l * right_counts[l] for l in left)

    print(f"The similarity score is: {similarity_score}!!")

# test
print(40*"-")
print("test!")
left, right = read_lists("./test_input.txt")
compute_similarity_score(left, right)

# part 2
print(40*"-")
print("Part 2!")
left, right = read_lists("./input_1.txt")
compute_similarity_score(left, right)
