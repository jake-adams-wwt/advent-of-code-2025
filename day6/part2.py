# Day 6 - Part 2
# Determine how many positions a single new obstacle '#' could be placed
# to trap the guard in an infinite loop.
# Only positions on the guard's original patrol path are candidates.
# The guard's starting position cannot be used for the new obstacle.


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
    # Directions: up, right, down, left (clockwise order)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    idx = directions.index(direction)
    return directions[(idx + 1) % 4]


def isInBounds(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def getPatrolPath(grid):
    """Return the set of positions visited by the guard on the original path."""
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)  # Facing up initially

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
    """Return True if placing an obstacle at (obstacle_r, obstacle_c) causes a loop."""
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)  # Facing up initially

    # Track (position, direction) states to detect a loop
    seen_states = set()
    seen_states.add((guard_r, guard_c, direction))

    while True:
        next_r = guard_r + direction[0]
        next_c = guard_c + direction[1]

        if not isInBounds(next_r, next_c, grid):
            return False

        if grid[next_r][next_c] == "#" or (next_r == obstacle_r and next_c == obstacle_c):
            # Obstacle ahead (existing or new): turn right without moving
            direction = turnRight(direction)
        else:
            guard_r, guard_c = next_r, next_c

        state = (guard_r, guard_c, direction)
        if state in seen_states:
            return True
        seen_states.add(state)


def countLoopPositions(grid):
    """Count candidate obstacle positions that cause the guard to loop."""
    guard_r, guard_c = findGuard(grid)

    # Only test positions on the guard's original patrol path (excluding start)
    patrol_path = getPatrolPath(grid)
    patrol_path.discard((guard_r, guard_c))

    loop_count = 0
    for r, c in patrol_path:
        if grid[r][c] == "." and causesLoop(grid, r, c):
            loop_count += 1

    return loop_count


def findAnswer(fileName):
    grid = readFileAsGrid(fileName)
    return countLoopPositions(grid)


testAnswer = findAnswer("test.txt")
print(f"Test answer: {testAnswer}")
assert testAnswer == 6

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
