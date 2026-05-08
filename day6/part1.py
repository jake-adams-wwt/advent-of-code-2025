# Day 6 - Part 1
# Simulate a guard patrolling a grid.
# The guard starts at '^' facing up, moves forward each step,
# and turns 90 degrees clockwise when an obstacle '#' is ahead.
# Count the number of distinct positions visited before the guard
# exits the grid.


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


def simulateGuard(grid):
    guard_r, guard_c = findGuard(grid)
    direction = (-1, 0)  # Facing up initially

    visited = set()
    visited.add((guard_r, guard_c))

    while True:
        next_r = guard_r + direction[0]
        next_c = guard_c + direction[1]

        if not isInBounds(next_r, next_c, grid):
            # Guard exits the grid
            break

        if grid[next_r][next_c] == "#":
            # Obstacle ahead: turn right without moving
            direction = turnRight(direction)
        else:
            # Move forward
            guard_r, guard_c = next_r, next_c
            visited.add((guard_r, guard_c))

    return len(visited)


def findAnswer(fileName):
    grid = readFileAsGrid(fileName)
    return simulateGuard(grid)


testAnswer = findAnswer("test.txt")
print(f"Test answer: {testAnswer}")
assert testAnswer == 41

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
