"""Comprehensive test suite for Day 6: Guard Gallivant.

Tests cover:
- File I/O and grid parsing
- Guard detection and positioning
- Boundary checking
- Guard simulation and patrol tracking
- Loop detection
- Obstacle placement and loop-causing positions
"""

import sys
import os
import copy

# Allow importing from the day6 directory regardless of where tests are run from
DAY6_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DAY6_DIR)

from part1 import (
    read_file_as_grid,
    find_guard,
    is_in_bounds,
    simulate_guard,
)
from part2 import causes_loop

TEST_FILE = os.path.join(DAY6_DIR, "test.txt")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_grid(lines):
    """Build a grid from a list of strings.

    Args:
        lines: List of strings representing grid rows.

    Returns:
        2D list (list of lists) representing the grid.
    """
    return [list(line) for line in lines]


# ---------------------------------------------------------------------------
# read_file_as_grid
# ---------------------------------------------------------------------------

def test_read_file_as_grid_returns_list_of_lists():
    grid = read_file_as_grid(TEST_FILE)
    assert isinstance(grid, list)
    assert all(isinstance(row, list) for row in grid)
    print("PASS test_read_file_as_grid_returns_list_of_lists")


def test_read_file_as_grid_dimensions():
    grid = read_file_as_grid(TEST_FILE)
    assert len(grid) == 10, f"Expected 10 rows, got {len(grid)}"
    assert len(grid[0]) == 10, f"Expected 10 cols, got {len(grid[0])}"
    print("PASS test_read_file_as_grid_dimensions")


# ---------------------------------------------------------------------------
# find_guard
# ---------------------------------------------------------------------------

def test_find_guard_up():
    grid = make_grid([".....", "..^..", "....."])
    row, col, dir_index = find_guard(grid)
    assert row == 1
    assert col == 2
    assert dir_index == 0  # up
    print("PASS test_find_guard_up")


def test_find_guard_right():
    grid = make_grid([".....", "..>..", "....."])
    row, col, dir_index = find_guard(grid)
    assert dir_index == 1  # right
    print("PASS test_find_guard_right")


def test_find_guard_down():
    grid = make_grid([".....", "..v..", "....."])
    row, col, dir_index = find_guard(grid)
    assert dir_index == 2  # down
    print("PASS test_find_guard_down")


def test_find_guard_left():
    grid = make_grid([".....", "..<..", "....."])
    row, col, dir_index = find_guard(grid)
    assert dir_index == 3  # left
    print("PASS test_find_guard_left")


def test_find_guard_test_file():
    grid = read_file_as_grid(TEST_FILE)
    row, col, dir_index = find_guard(grid)
    assert row == 6
    assert col == 4
    assert dir_index == 0  # facing up
    print("PASS test_find_guard_test_file")


# ---------------------------------------------------------------------------
# is_in_bounds
# ---------------------------------------------------------------------------

def test_is_in_bounds_inside():
    grid = make_grid(["...", "...", "..."])
    assert is_in_bounds(0, 0, grid)
    assert is_in_bounds(1, 1, grid)
    assert is_in_bounds(2, 2, grid)
    print("PASS test_is_in_bounds_inside")


def test_is_in_bounds_outside():
    grid = make_grid(["...", "...", "..."])
    assert not is_in_bounds(-1, 0, grid)
    assert not is_in_bounds(0, -1, grid)
    assert not is_in_bounds(3, 0, grid)
    assert not is_in_bounds(0, 3, grid)
    print("PASS test_is_in_bounds_outside")


# ---------------------------------------------------------------------------
# simulate_guard
# ---------------------------------------------------------------------------

def test_simulate_guard_exits_immediately():
    # Guard at top row facing up — exits on first step
    grid = make_grid(["..^..", "....."])
    visited = simulate_guard(grid)
    assert visited is not None
    assert (0, 2) in visited
    print("PASS test_simulate_guard_exits_immediately")


def test_simulate_guard_turns_right_on_obstacle():
    # Guard faces up, obstacle directly above — should turn right then walk right
    grid = make_grid(["..#..", "..^..", "....."])
    visited = simulate_guard(grid)
    assert visited is not None
    # Guard starts at (1,2), turns right (east), walks off right edge
    assert (1, 2) in visited
    assert (1, 3) in visited
    assert (1, 4) in visited
    print("PASS test_simulate_guard_turns_right_on_obstacle")


def test_simulate_guard_visits_all_positions_in_corridor():
    # Guard walks straight up a clear column and exits
    grid = make_grid([".....", ".....", "..^..", "....."])
    visited = simulate_guard(grid)
    assert visited is not None
    assert (2, 2) in visited
    assert (1, 2) in visited
    assert (0, 2) in visited
    print("PASS test_simulate_guard_visits_all_positions_in_corridor")


def test_simulate_guard_detects_loop():
    # Guard is boxed in by four obstacles and loops forever:
    #   .#.   row 0: obstacle at col 1
    #   #.#   row 1: obstacles at col 0 and col 2
    #   .^.   row 2: guard at (2,1) facing up
    #   .#.   row 3: obstacle at col 1
    # Trace: (2,1)^->(1,1) blocked by (0,1) turn right ->
    #        blocked by (1,2) turn right (south) ->
    #        (2,1) blocked by (3,1) turn right (west) ->
    #        blocked by (1,0) turn right (north) ->
    #        back to (1,1) facing north = repeated state -> loop
    grid = make_grid([".#.", "#.#", ".^.", ".#."])
    result = simulate_guard(grid)
    assert result is None, "Expected loop detection (None), got visited set"
    print("PASS test_simulate_guard_detects_loop")


def test_simulate_guard_no_duplicate_positions():
    # Visited positions should be a set — no duplicates by definition
    grid = read_file_as_grid(TEST_FILE)
    visited = simulate_guard(grid)
    assert visited is not None
    assert len(visited) == len(set(visited))  # trivially true for a set
    print("PASS test_simulate_guard_no_duplicate_positions")


def test_simulate_guard_part1_test_answer():
    grid = read_file_as_grid(TEST_FILE)
    visited = simulate_guard(grid)
    assert visited is not None
    assert len(visited) == 41, f"Expected 41, got {len(visited)}"
    print("PASS test_simulate_guard_part1_test_answer")


# ---------------------------------------------------------------------------
# causes_loop
# ---------------------------------------------------------------------------

def test_causes_loop_no_loop_on_empty_cell():
    # Placing an obstacle far from the path should not cause a loop
    grid = read_file_as_grid(TEST_FILE)
    # Row 9, col 9 is never visited — adding an obstacle there changes nothing
    assert not causes_loop(grid, 9, 9)
    print("PASS test_causes_loop_no_loop_on_empty_cell")


def test_causes_loop_known_loop_positions():
    # The six known loop-causing positions from the test grid
    loop_positions = [
        (6, 3),
        (7, 6),
        (7, 7),
        (8, 1),
        (8, 3),
        (9, 7),
    ]
    grid = read_file_as_grid(TEST_FILE)
    for row, col in loop_positions:
        assert causes_loop(grid, row, col), (
            f"Expected obstacle at ({row},{col}) to cause a loop"
        )
    print("PASS test_causes_loop_known_loop_positions")


def test_causes_loop_does_not_mutate_original_grid():
    grid = read_file_as_grid(TEST_FILE)
    original_snapshot = [row[:] for row in grid]
    causes_loop(grid, 6, 3)
    assert grid == original_snapshot, "causes_loop must not mutate the original grid"
    print("PASS test_causes_loop_does_not_mutate_original_grid")


# ---------------------------------------------------------------------------
# Part 2 integration
# ---------------------------------------------------------------------------

def test_part2_test_answer():
    # Import find_answer from part2 directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "part2_module", os.path.join(DAY6_DIR, "part2.py")
    )
    part2 = importlib.util.module_from_spec(spec)
    # Patch open so find_answer uses the test file
    original_dir = os.getcwd()
    os.chdir(DAY6_DIR)
    try:
        # Re-run find_answer directly
        from part2 import find_answer
        result = find_answer(TEST_FILE)
        assert result == 6, f"Expected 6, got {result}"
        print("PASS test_part2_test_answer")
    finally:
        os.chdir(original_dir)


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_read_file_as_grid_returns_list_of_lists()
    test_read_file_as_grid_dimensions()
    test_find_guard_up()
    test_find_guard_right()
    test_find_guard_down()
    test_find_guard_left()
    test_find_guard_test_file()
    test_is_in_bounds_inside()
    test_is_in_bounds_outside()
    test_simulate_guard_exits_immediately()
    test_simulate_guard_turns_right_on_obstacle()
    test_simulate_guard_visits_all_positions_in_corridor()
    test_simulate_guard_detects_loop()
    test_simulate_guard_no_duplicate_positions()
    test_simulate_guard_part1_test_answer()
    test_causes_loop_no_loop_on_empty_cell()
    test_causes_loop_known_loop_positions()
    test_causes_loop_does_not_mutate_original_grid()
    test_part2_test_answer()
    print("\nAll tests passed!")
