def read_file_as_grid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines() if line.strip()]


def has_paper(x, y, grid):
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == "@"


def is_isolated(x, y, grid):
    """Return True if the cell at (x, y) is an '@' with no cardinal '@' neighbours."""
    if not has_paper(x, y, grid):
        return False

    cardinal_neighbours = [
        has_paper(x, y - 1, grid),  # up
        has_paper(x, y + 1, grid),  # down
        has_paper(x - 1, y, grid),  # left
        has_paper(x + 1, y, grid),  # right
    ]

    return not any(cardinal_neighbours)


def find_answer(filename):
    """Count all '@' cells that have no cardinal '@' neighbours."""
    grid = read_file_as_grid(filename)
    isolated_count = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if is_isolated(x, y, grid):
                print(f"Found isolated paper at ({x}, {y})")
                isolated_count += 1

    return isolated_count


test_answer = find_answer("test.txt")
print(f"Test answer: {test_answer}")
assert test_answer == 4

answer = find_answer("input.txt")
print(f"Answer: {answer}")
