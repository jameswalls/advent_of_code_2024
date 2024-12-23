import pdb
from enum import Enum

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"

class Guard:
    def __init__(self, row: int, col: int, direction: str) -> None:
        self.location: tuple[int, int] = row, col
        mapped_direction = {
            "^": Direction.UP,
            "v": Direction.DOWN,
            ">": Direction.LEFT,
            "<": Direction.RIGHT,
        }[direction]
        self.direction: Direction = mapped_direction

        self.original_direciton = direction

    def next_location(self):
        match self.direction:
            case Direction.UP:
                return self.location[0] - 1, self.location[1]
            case Direction.DOWN:
                return self.location[0] + 1, self.location[1]
            case Direction.RIGHT:
                return self.location[0], self.location[1] + 1
            case Direction.LEFT:
                return self.location[0], self.location[1] - 1

    def turn_around(self):
        "Every now and then I get a little..."
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.RIGHT:
                self.direction = Direction.DOWN
            case Direction.LEFT:
                self.direction = Direction.UP


    def set_location(self, location: tuple[int, int]):
        self.location = location

    def set_direction(self, direction: Direction):
        self.direction = direction

    def get_location(self) -> tuple[int, int]:
        return self.location

class Grid:
    def __init__(self, path: str) -> None:
        self.object_locations = set()
        with open(path, "r") as file:
            for row, line in enumerate(file.readlines()):
                for col, char in enumerate(list(line.strip())):
                    match char:
                        case ".": continue
                        case "#": self.object_locations.add((row, col))
                        case "^" | "v" | ">" | "<": self.guard = Guard(row, col, char)
                        case _: raise Exception(f"Unrecognized char {char}")

        self.max_row = row
        self.max_col = col
        assert self.guard
        self.visited_locations = [self.guard.location]

    def run(self): 
        while self.is_valid_location(next_location := self.guard.next_location()):
            if next_location in self.object_locations:
                self.guard.turn_around()
                continue
            self.guard.set_location(next_location)
            self.visited_locations.append(self.guard.get_location())

    def is_valid_location(self, location: tuple[int, int]) -> bool:
        return (0 <= location[0] <= self.max_row) and (0 <= location[1] <= self.max_col)

    def draw_path(self):
        output = [["." for _ in range(self.max_col+1)] for _ in range(self.max_row+1)]
        for row, col in self.visited_locations:
            output[row][col] = "X"
        for row, col in self.object_locations:
            output[row][col] = "#"

        output[self.visited_locations[0][0]][self.visited_locations[0][1]] = self.guard.original_direciton
        with open("./output.txt", "w") as file:
            for line in output:
                file.write("".join(line)+"\n")

if __name__ == "__main__":
    grid = Grid("./example.txt")
    grid.run()
    print("test")
    print(f"Unique visited locations: {len(set(grid.visited_locations))}")
    grid.draw_path()

    grid = Grid("./part1.txt")
    grid.run()
    print("part1")
    print(f"Unique visited locations: {len(set(grid.visited_locations))}")
    grid.draw_path()
