import pdb
from abc import ABC, abstractmethod
from itertools import product

with open("./part1.txt") as file:
    equations: list[tuple[int, list[int]]] = []
    for line in file.readlines():
        result, operands = line.split(":")
        equations.append((int(result), [int(i) for i in operands.strip().split()]))

class Operation(ABC):
    @abstractmethod
    def __call__(self, x: int, y: int) -> int: ...

class Add(Operation):
    def __str__(self) -> str:
        return "+"

    def __repr__(self) -> str:
        return "+"

    def __call__(self, x: int, y: int) -> int:
        return x + y

class Mult(Operation):
    def __str__(self) -> str:
        return "*"

    def __repr__(self) -> str:
        return "*"

    def __call__(self, x: int, y: int) -> int:
        return x * y

class Concat(Operation):
    def __str__(self) -> str:
        return "||"

    def __repr__(self) -> str:
        return "||"

    def __call__(self, x: int, y: int) -> int:
        return int("{}{}".format(x, y))

def reduce(operands: list[int], operations: list[Operation], value: int|None=None) -> int:
    if not value:
        return reduce(operands[1:], operations, operands[0])
    elif operations:
        next_operand = operands[0]
        f = operations[0]
        # print("{}{}{}".format(value, f, next_operand))
        return reduce(operands[1:], operations[1:], f(value, next_operand))
    else:
        return value
        
add = Add()
mult = Mult()
concat = Concat()

total_calibration_result = 0
for result, operands in equations:
    for operations in product([add, mult, concat], repeat=len(operands)-1):
        o = operands.copy()
        output = reduce(operands, list(operations))
        if result == output:
            total_calibration_result += result
            break

print(f"total_calibration_result: {total_calibration_result}")
