from collections import defaultdict
from enum import Enum, auto
import pdb

class Direction(Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"

class Passing(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"

    @classmethod
    def from_direction(cls, direction: Direction) -> "Passing":
        passing = {
            Direction.UP: Passing.VERTICAL,
            Direction.DOWN: Passing.VERTICAL,
            Direction.LEFT: Passing.HORIZONTAL,
            Direction.RIGHT: Passing.HORIZONTAL,
        }[direction]

        return passing

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

        self.original_location = row, col
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

    def get_direction(self) -> Direction:
        return self.direction

class Grid:
    def __init__(self, path: str) -> None:
        self.object_locations = set()
        with open(path, "r") as file:
            lines = file.readlines()

        for row, line in enumerate(lines):
            for col, char in enumerate(list(line.strip())):
                match char:
                    case ".": continue
                    case "#": self.object_locations.add((row, col))
                    case "^" | "v" | ">" | "<": self.guard = Guard(row, col, char)
                    case _: raise Exception(f"Unrecognized char {char}")

        self.max_row = row
        self.max_col = col
        assert self.guard
        self.visited_locations = defaultdict(lambda: [])
        starting_location = self.guard.get_location()
        self.visited_locations[starting_location].append({"arrived": None, "left": None})
        self.path = [starting_location]
        self.new_objects = []

    def add_object_location(self, loc: tuple[int, int]):
        if loc not in self.object_locations:
            self.object_locations.add(loc)
            self.new_objects.append(loc)

    def run(self): 
        while self.is_valid_location(next_location := self.guard.next_location()):
            if next_location in self.object_locations:
                self.guard.turn_around()
                continue
            current_direction = self.guard.get_direction()
            self.visited_locations[self.guard.get_location()][-1]["left"] = current_direction
            self.guard.set_location(next_location)
            self.visited_locations[next_location].append({"arrived": current_direction})

        self.visited_locations = dict(self.visited_locations)

    def run_with_loop_detection(self) -> bool:
        while self.is_valid_location(next_location := self.guard.next_location()):
            if next_location in self.object_locations:
                self.guard.turn_around()
                continue
            current_direction = self.guard.get_direction()
            self.visited_locations[self.guard.get_location()][-1]["left"] = current_direction
            self.guard.set_location(next_location)
            visited_loc_directions = self.visited_locations[next_location]
            for visited_loc_direction in visited_loc_directions:
                if visited_loc_direction["arrived"] == current_direction:
                    return True
            else:
                visited_loc_directions.append({"arrived": current_direction})

        return False

    def iter_adjacent_locations(self, loc: tuple[int, int]):
        # todo: take into account direction to yield locations.
        #       if moving vertically, horizontal locations should not
        #       be added.
        row, col = loc
        if (prev_row := row - 1 ) >= 0:
            yield prev_row, col

        if (next_row := row + 1 ) <= self.max_row:
            yield next_row, col

        if (prev_col := col - 1 ) > 0:
            yield row, prev_col

        if (next_col := col + 1 ) <= self.max_col:
            yield row, next_col

    def is_valid_location(self, location: tuple[int, int]) -> bool:
        return (0 <= location[0] <= self.max_row) and (0 <= location[1] <= self.max_col)

    def total_unique_visited_locations(self) -> int:
        return len(self.visited_locations.keys())

    def draw_path(self, path: str|None=None):
        output = [["." for _ in range(self.max_col+1)] for _ in range(self.max_row+1)]
        for row, col, char in self.visited_locations_chars():
            output[row][col] = char
        for row, col in self.object_locations:
            if (row, col) in self.new_objects:
                output[row][col] = "O"
            else:
                output[row][col] = "#"

        _path = path or "output.txt"
        with open(_path, "w") as file:
            for line in output:
                file.write("".join(line)+"\n")

    def visited_locations_chars(self):
        for (row, col), passings in self.visited_locations.items():
            mapped_passings = []
            for passing in passings:
                if not passing.get("arrived"):
                    mapped_passings.append(passing["left"].value)
                    continue
                elif not passing.get("left"):
                    match Passing.from_direction(passing["arrived"]):
                        case Passing.VERTICAL: mapped_passings.append("|")
                        case Passing.HORIZONTAL: mapped_passings.append("-")
                    continue

                arrived = Passing.from_direction(passing["arrived"])
                left = Passing.from_direction(passing["left"])
                
                match arrived, left:
                    case Passing.VERTICAL, Passing.VERTICAL:
                        mapped_passings.append("|")
                    case Passing.HORIZONTAL, Passing.HORIZONTAL:
                        mapped_passings.append("-")
                    case _:
                        mapped_passings.append("+")
            char = self.find_dominant_char(mapped_passings)
            yield row, col, char

    @staticmethod
    def find_dominant_char(mapped_passings: list[str]) -> str:
        current_char = mapped_passings[0]
        for char in mapped_passings[1:]:
            if current_char in ["^", "v", ">", "<", "+"]:
                return current_char

            if current_char != char:
                return "+"

            current_char = char

        return current_char

    def get_candidate_blocker_locations(self):
        blockers = set()
        for loc in self.visited_locations.keys():
            row, col = loc
            blockers.add(loc)

            upper_row = loc[0] - 1
            upper_loc = upper_row, col
            if upper_row >= 0 and (upper_loc not in self.object_locations):
                blockers.add(upper_loc)

            lower_row = loc[0] + 1
            lower_loc = lower_row, col
            if lower_row <= self.max_row and (lower_loc not in self.object_locations):
                blockers.add((upper_row, col))

            left_col = loc[1] - 1
            left_loc = row, left_col
            if left_col >= 0 and (left_loc not in self.object_locations):
                blockers.add(left_loc)

            right_col = loc[1] - 1
            right_loc = row, right_col
            if left_col <= self.max_col and (right_loc not in self.object_locations):
                blockers.add(left_loc)

        blockers.remove(self.guard.original_location)

        return blockers

if __name__ == "__main__":
    grid = Grid("./example.txt")
    grid.run()
    print("test")
    print(f"Unique visited locations: {grid.total_unique_visited_locations()}")

    total_blocks = 0
    for new_object_loc in grid.get_candidate_blocker_locations():
        test_grid = Grid("./example.txt")
        test_grid.add_object_location(new_object_loc)
        if test_grid.run_with_loop_detection():
            total_blocks += 1
            test_grid.draw_path(str(new_object_loc))
    print(f"total blocks: {total_blocks}")

    grid = Grid("./part1.txt")
    grid.run()
    print("part 2")
    print(f"Unique visited locations: {grid.total_unique_visited_locations()}")

    total_blocks = 0
    for new_object_loc in grid.get_candidate_blocker_locations():
        test_grid = Grid("./part1.txt")
        test_grid.add_object_location(new_object_loc)
        if test_grid.run_with_loop_detection():
            total_blocks += 1
    print(f"total blocks: {total_blocks}")
