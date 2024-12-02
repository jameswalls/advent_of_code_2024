from itertools import pairwise

def count_safe_reports(path: str):
    reports = []
    with open(path, "r") as file:
        for line in file.readlines():
            reports.append([int(i) for i in line.split()])

    safe_reports = 0
    for report in reports:
        differences = [j - i for i, j in pairwise(report)]
        all_increasing = all(i>0 for i in differences)
        all_decreasing = all(i<0 for i in differences)
        between_one_three = all( 1<=abs(i)<=3 for i in differences)

        if (all_increasing or all_decreasing) and between_one_three:
            safe_reports += 1
    print(f"Total safe reports: {safe_reports}")

# test
print(40*"-")
print("test")
count_safe_reports("./test.txt")

# part 1
print(40*"-")
print("part 1")
count_safe_reports("./part_1.txt")
