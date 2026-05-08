def read_file_as_grid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines() if line.strip()]


def has_paper(x, y, grid):
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == "@"


def count_cardinal_paper_neighbours(x, y, grid):
    """Return the number of cardinal '@' neighbours for cell (x, y)."""
    return sum([
        has_paper(x, y - 1, grid),  # up
        has_paper(x, y + 1, grid),  # down
        has_paper(x - 1, y, grid),  # left
        has_paper(x + 1, y, grid),  # right
    ])


def spread_once(grid):
    """Spread '@' to every empty cell that has exactly one cardinal '@' neighbour.

    Returns the number of cells that were converted in this pass.
    """
    to_spread = []

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "." and count_cardinal_paper_neighbours(x, y, grid) == 1:
                to_spread.append((x, y))

    for x, y in to_spread:
        print(f"Spreading paper to ({x}, {y})")
        grid[y][x] = "@"

    return len(to_spread)


def find_answer(filename):
    """Repeatedly spread '@' to cells with exactly one cardinal '@' neighbour.

    Returns the total number of cells converted across all rounds.
    """
    grid = read_file_as_grid(filename)
    total_spread = 0
    round_number = 1

    while True:
        spread_count = spread_once(grid)
        print(f"Round {round_number}: spread {spread_count} cell(s)")
        if spread_count == 0:
            break
        total_spread += spread_count
        round_number += 1

    return total_spread


test_answer = find_answer("test.txt")
print(f"Test answer: {test_answer}")
assert test_answer == 4

answer = find_answer("input.txt")
print(f"Answer: {answer}")
