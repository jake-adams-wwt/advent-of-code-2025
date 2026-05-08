"""Day 6: Guard Gallivant - Part 2

Find all positions where placing a single obstacle would cause the guard
to enter an infinite loop. The guard starts at a position marked with a
direction (^, >, v, <) and moves forward until hitting an obstacle (#),
at which point it turns right. We need to count how many positions on the
guard's original path, when blocked, would cause a loop.
"""

import copy

# Direction vectors: up, right, down, left (turn right = next index)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIRECTION_CHARS = {"^": 0, ">": 1, "v": 2, "<": 3}


def read_file_as_grid(filename):
    """Read a file and return it as a 2D grid (list of lists).

    Args:
        filename: Path to the input file.

    Returns:
        A 2D list where each element is a character from the file.
    """
    with open(filename, "r") as f:
        return [list(line.rstrip("\n")) for line in f.readlines()]


def find_guard(grid):
    """Find the guard's starting position and direction in the grid.

    Args:
        grid: 2D list representing the patrol area.

    Returns:
        Tuple of (row, col, direction_index) where direction_index is 0-3.

    Raises:
        ValueError: If no guard is found in the grid.
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in DIRECTION_CHARS:
                return row, col, DIRECTION_CHARS[grid[row][col]]
    raise ValueError("No guard found in grid")


def is_in_bounds(row, col, grid):
    """Check if a position is within the grid bounds.

    Args:
        row: Row index.
        col: Column index.
        grid: 2D list representing the grid.

    Returns:
        True if the position is within bounds, False otherwise.
    """
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def simulate_guard(grid):
    """Simulate the guard's patrol and return the set of visited positions.

    Args:
        grid: 2D list representing the patrol area.

    Returns:
        Set of (row, col) tuples representing visited positions.
        Returns None if the guard enters an infinite loop.
    """
    row, col, dir_index = find_guard(grid)
    visited = set()
    states_seen = set()

    while is_in_bounds(row, col, grid):
        state = (row, col, dir_index)
        if state in states_seen:
            return None  # Infinite loop detected
        states_seen.add(state)
        visited.add((row, col))

        dr, dc = DIRECTIONS[dir_index]
        next_row, next_col = row + dr, col + dc

        if is_in_bounds(next_row, next_col, grid) and grid[next_row][next_col] == "#":
            # Turn right 90 degrees
            dir_index = (dir_index + 1) % 4
        else:
            row, col = next_row, next_col

    return visited


def causes_loop(grid, obstacle_row, obstacle_col):
    """Check if placing an obstacle at a position causes a loop.

    Args:
        grid: 2D list representing the patrol area.
        obstacle_row: Row index where obstacle would be placed.
        obstacle_col: Column index where obstacle would be placed.

    Returns:
        True if placing the obstacle causes an infinite loop, False otherwise.
    """
    modified_grid = copy.deepcopy(grid)
    modified_grid[obstacle_row][obstacle_col] = "#"
    return simulate_guard(modified_grid) is None


def find_answer(file_name):
    """Find the number of positions that would cause a loop if blocked.

    Args:
        file_name: Path to the input file.

    Returns:
        The count of positions that would cause a loop.
    """
    grid = read_file_as_grid(file_name)
    guard_row, guard_col, _ = find_guard(grid)

    # Only candidate positions are those on the guard's original patrol path
    original_path = simulate_guard(grid)

    loop_count = 0
    for row, col in original_path:
        # Cannot place obstacle on the guard's starting position
        if row == guard_row and col == guard_col:
            continue
        # Cannot place obstacle where one already exists
        if grid[row][col] == "#":
            continue
        if causes_loop(grid, row, col):
            loop_count += 1

    return loop_count


if __name__ == "__main__":
    test_answer = find_answer("test.txt")
    print(f"Test answer: {test_answer}")
    assert test_answer == 6, f"Expected 6, got {test_answer}"

    answer = find_answer("input.txt")
    print(f"Answer: {answer}")
