from itertools import pairwise

def load_reports(path: str) -> list[list[int]]:
    reports = []
    with open(path, "r") as file:
        for line in file.readlines():
            reports.append([int(i) for i in line.split()])

    return reports

def check_conditions(report: list[int]) -> bool:
    differences = [j - i for i, j in pairwise(report)]
    all_increasing = all(i>0 for i in differences)
    all_decreasing = all(i<0 for i in differences)
    between_one_three = all( 1<=abs(i)<=3 for i in differences)

    return (all_increasing or all_decreasing) and between_one_three

def is_safe_with_removal(report: list[int], i: int) -> bool:
    if i == len(report):
        return False
    else:
        sub_report = report[:i] + report[i+1:]
        return check_conditions(sub_report) or is_safe_with_removal(report, i+1)
    
def is_safe_report(report: list[int]) -> bool:
    return check_conditions(report) or is_safe_with_removal(report, 0)

# test
print(40*"-")
print("test")
reports = load_reports("./test.txt")
safe_reports = sum(is_safe_report(report) for report in reports)
print(f"Total safe reports: {safe_reports}")

# part 1
print(40*"-")
print("part 1")
reports = load_reports("./part_1.txt")
safe_reports = sum(is_safe_report(report) for report in reports)
print(f"Total safe reports: {safe_reports}")
