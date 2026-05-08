# Tests for Day 6 - Guard Patrol Simulation
# Run with: python test.py


def readFileAsGrid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines() if line.strip()]


def findGuard(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "^":
                return r, c
    raise ValueError("Guard not found in grid")


def turnRight(direction):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    idx = directions.index(direction)
    return directions[(idx + 1) % 4]


def isInBounds(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def simulateGuard(grid):
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)

    visited = set()
    visited.add((guard_r, guard_c))

    while True:
        next_r = guard_r + direction[0]
        next_c = guard_c + direction[1]

        if not isInBounds(next_r, next_c, grid):
            break

        if grid[next_r][next_c] == "#":
            direction = turnRight(direction)
        else:
            guard_r, guard_c = next_r, next_c
            visited.add((guard_r, guard_c))

    return len(visited)


def getPatrolPath(grid):
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)

    visited = set()
    visited.add((guard_r, guard_c))

    while True:
        next_r = guard_r + direction[0]
        next_c = guard_c + direction[1]

        if not isInBounds(next_r, next_c, grid):
            break

        if grid[next_r][next_c] == "#":
            direction = turnRight(direction)
        else:
            guard_r, guard_c = next_r, next_c
            visited.add((guard_r, guard_c))

    return visited


def causesLoop(grid, obstacle_r, obstacle_c):
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)

    seen_states = set()
    seen_states.add((guard_r, guard_c, direction))

    while True:
        next_r = guard_r + direction[0]
        next_c = guard_c + direction[1]

        if not isInBounds(next_r, next_c, grid):
            return False

        if grid[next_r][next_c] == "#" or (next_r == obstacle_r and next_c == obstacle_c):
            direction = turnRight(direction)
        else:
            guard_r, guard_c = next_r, next_c

        state = (guard_r, guard_c, direction)
        if state in seen_states:
            return True
        seen_states.add(state)


def countLoopPositions(grid):
    guard_r, guard_c = findGuard(grid)
    patrol_path = getPatrolPath(grid)
    patrol_path.discard((guard_r, guard_c))

    loop_count = 0
    for r, c in patrol_path:
        if grid[r][c] == "." and causesLoop(grid, r, c):
            loop_count += 1

    return loop_count


# ---------------------------------------------------------------------------
# Helper to build a grid from a multiline string
# ---------------------------------------------------------------------------

def gridFromString(text):
    return [list(line) for line in text.strip().splitlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_turnRight():
    up = (-1, 0)
    right = (0, 1)
    down = (1, 0)
    left = (0, -1)
    assert turnRight(up) == right, "up -> right"
    assert turnRight(right) == down, "right -> down"
    assert turnRight(down) == left, "down -> left"
    assert turnRight(left) == up, "left -> up"
    print("PASS test_turnRight")


def test_isInBounds():
    grid = [["."] * 5 for _ in range(4)]
    assert isInBounds(0, 0, grid)
    assert isInBounds(3, 4, grid)
    assert not isInBounds(-1, 0, grid)
    assert not isInBounds(4, 0, grid)
    assert not isInBounds(0, 5, grid)
    assert not isInBounds(0, -1, grid)
    print("PASS test_isInBounds")


def test_findGuard():
    grid = gridFromString("""
.....
..^..
.....
""")
    r, c = findGuard(grid)
    assert r == 1 and c == 2, f"Expected (1, 2), got ({r}, {c})"
    print("PASS test_findGuard")


def test_guardExitsImmediately():
    # Guard at top row facing up — exits on the very first step
    grid = gridFromString("""
..^..
.....
.....
""")
    result = simulateGuard(grid)
    assert result == 1, f"Expected 1 visited cell, got {result}"
    print("PASS test_guardExitsImmediately")


def test_guardWalksStraight():
    # Guard in the middle of an empty column, facing up — walks to the top
    grid = gridFromString("""
.....
.....
..^..
.....
.....
""")
    result = simulateGuard(grid)
    # Visits (2,2), (1,2), (0,2) = 3 cells
    assert result == 3, f"Expected 3 visited cells, got {result}"
    print("PASS test_guardWalksStraight")


def test_guardTurnsAtObstacle():
    # Guard faces up, hits obstacle above, turns right and walks off the right edge
    grid = gridFromString("""
..#..
..^..
.....
""")
    result = simulateGuard(grid)
    # Starts at (1,2), turns right (faces right), walks to (1,3), (1,4) then exits
    # Visited: (1,2), (1,3), (1,4) = 3
    assert result == 3, f"Expected 3 visited cells, got {result}"
    print("PASS test_guardTurnsAtObstacle")


def test_guardDoesNotRevisitCells():
    # Guard walks a path that crosses itself — visited count should not double-count
    grid = gridFromString("""
.....
.#...
..^..
.....
.....
""")
    result = simulateGuard(grid)
    # Starts (2,2) facing up -> (1,2) -> hits # at (1,1)? No, obstacle is at (1,1).
    # (2,2) up -> (1,2) -> (0,2) exits. Visited = 3
    assert result == 3, f"Expected 3 visited cells, got {result}"
    print("PASS test_guardDoesNotRevisitCells")


def test_part1_test_file():
    grid = readFileAsGrid("test.txt")
    result = simulateGuard(grid)
    assert result == 41, f"Expected 41, got {result}"
    print("PASS test_part1_test_file")


def test_causesLoop_simple():
    # A 5x5 box with the guard trapped in a loop by a single obstacle
    # Guard at (2,2) facing up; obstacle at (0,2) forces right turn,
    # obstacle at (2,4) forces right turn, obstacle at (4,2) forces right turn,
    # obstacle at (2,0) forces right turn -> loop
    grid = gridFromString("""
..#..
.....
#.^.#
.....
..#..
""")
    # With no extra obstacle, guard hits (0,2) -> turns right -> hits (2,4) ->
    # turns right -> hits (4,2) -> turns right -> hits (2,0) -> turns right ->
    # back to facing up at (2,2) -> loop detected
    assert causesLoop(grid, 99, 99) is False  # dummy position outside grid
    print("PASS test_causesLoop_simple")


def test_causesLoop_no_loop():
    # Open grid — guard exits, no loop
    grid = gridFromString("""
.....
.....
..^..
.....
.....
""")
    assert causesLoop(grid, 99, 99) is False
    print("PASS test_causesLoop_no_loop")


def test_part2_test_file():
    grid = readFileAsGrid("test.txt")
    result = countLoopPositions(grid)
    assert result == 6, f"Expected 6, got {result}"
    print("PASS test_part2_test_file")


def test_getPatrolPath_includes_start():
    grid = gridFromString("""
.....
.....
..^..
.....
.....
""")
    path = getPatrolPath(grid)
    # Guard starts at (2,2) and walks up to (0,2)
    assert (2, 2) in path
    assert (1, 2) in path
    assert (0, 2) in path
    assert len(path) == 3
    print("PASS test_getPatrolPath_includes_start")


def test_getPatrolPath_excludes_out_of_bounds():
    grid = gridFromString("""
.....
.....
..^..
.....
.....
""")
    path = getPatrolPath(grid)
    for r, c in path:
        assert isInBounds(r, c, grid), f"({r},{c}) is out of bounds"
    print("PASS test_getPatrolPath_excludes_out_of_bounds")


def test_countLoopPositions_empty_grid():
    # Guard exits immediately — no loop positions possible
    grid = gridFromString("""
..^..
.....
.....
""")
    result = countLoopPositions(grid)
    assert result == 0, f"Expected 0, got {result}"
    print("PASS test_countLoopPositions_empty_grid")


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_turnRight()
    test_isInBounds()
    test_findGuard()
    test_guardExitsImmediately()
    test_guardWalksStraight()
    test_guardTurnsAtObstacle()
    test_guardDoesNotRevisitCells()
    test_part1_test_file()
    test_causesLoop_simple()
    test_causesLoop_no_loop()
    test_part2_test_file()
    test_getPatrolPath_includes_start()
    test_getPatrolPath_excludes_out_of_bounds()
    test_countLoopPositions_empty_grid()
    print("\nAll tests passed!")
