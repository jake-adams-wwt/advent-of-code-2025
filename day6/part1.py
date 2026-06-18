def readFileAsGrid(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines() if line.strip()]


def findGuard(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in "^>v<":
                return x, y, grid[y][x]
    return None


# Direction order for turning right: up -> right -> down -> left -> up ...
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


def findAnswer(fileName):
    grid = readFileAsGrid(fileName)
    visited = simulateGuard(grid)
    return len(visited)


testAnswer = findAnswer("test.txt")
print(f"Test answer: {testAnswer}")
assert testAnswer == 41, f"Expected 41, got {testAnswer}"

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
