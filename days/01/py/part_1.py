def read_lists(path: str) -> tuple[list, list]:
    left_list = []
    right_list = []

    with open(path, "r") as file:
        for line in file.readlines():
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))

    left_list.sort()
    right_list.sort()

    return left_list, right_list

def total_difference(left: list, right: list):
    differences = [abs(l - r) for l, r in zip(left, right)]
    total_difference = sum(differences)

    print(f"The total distance is: {total_difference}!!")

# test
print(40*"-")
print("test!")
left, right = read_lists("./test_input.txt")
total_difference(left, right)

# part 1
print(40*"-")
print("part 1!")
left, right = read_lists("./input_1.txt")
total_difference(left, right)
