"""Helper script to generate a realistic day6/input.txt puzzle grid."""
import random

random.seed(42)

ROWS = 130
COLS = 130
OBSTACLE_DENSITY = 0.08  # ~8% of cells are obstacles

grid = [["." for _ in range(COLS)] for _ in range(ROWS)]

# Place obstacles randomly, avoiding the border cells
for r in range(ROWS):
    for c in range(COLS):
        if random.random() < OBSTACLE_DENSITY:
            grid[r][c] = "#"

# Place the guard somewhere in the middle area, facing up (^)
guard_r = ROWS // 2 - 10
guard_c = COLS // 2 + 5
grid[guard_r][guard_c] = "^"

with open("input.txt", "w") as f:
    for row in grid:
        f.write("".join(row) + "\n")

print(f"Generated {ROWS}x{COLS} grid with guard at ({guard_r}, {guard_c})")
