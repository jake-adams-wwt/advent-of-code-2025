def readFileAsGrid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines() if line.strip()]


def findGuard(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in "^>v<":
                return x, y, grid[y][x]
    return None


DIRECTIONS = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

TURN_RIGHT = {"^": ">", ">": "v", "v": "<", "<": "^"}


def simulateGuard(grid):
    """Simulate the guard's path. Returns set of visited (x, y) positions,
    or None if the guard loops forever."""
    x, y, direction = findGuard(grid)

    visited = set()
    visited_states = set()

    while True:
        state = (x, y, direction)
        if state in visited_states:
            return None  # Loop detected
        visited_states.add(state)
        visited.add((x, y))

        dx, dy = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        # Check if next position is out of bounds
        if ny < 0 or ny >= len(grid) or nx < 0 or nx >= len(grid[0]):
            break  # Guard leaves the grid

        # Check if next position is an obstacle
        if grid[ny][nx] == "#":
            direction = TURN_RIGHT[direction]  # Turn right
        else:
            x, y = nx, ny  # Move forward

    return visited


def causesLoop(grid, obstacleX, obstacleY):
    """Returns True if placing an obstacle at (obstacleX, obstacleY) causes a loop."""
    # Don't place on the guard's starting position
    gx, gy, _ = findGuard(grid)
    if obstacleX == gx and obstacleY == gy:
        return False

    # Temporarily place the obstacle
    original = grid[obstacleY][obstacleX]
    grid[obstacleY][obstacleX] = "#"

    result = simulateGuard(grid)

    # Restore the grid
    grid[obstacleY][obstacleX] = original

    return result is None  # None means a loop was detected


def findAnswer(fileName):
    grid = readFileAsGrid(fileName)

    # First, find all positions the guard visits in the original path
    # Only candidate positions for new obstacles are on the original path
    originalPath = simulateGuard(grid)

    loopCount = 0
    for (x, y) in originalPath:
        if grid[y][x] != "#":
            if causesLoop(grid, x, y):
                print(f"Placing obstacle at ({x}, {y}) causes a loop")
                loopCount += 1

    return loopCount


testAnswer = findAnswer("test.txt")
print(f"Test answer: {testAnswer}")
assert testAnswer == 6, f"Expected 6, got {testAnswer}"

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
