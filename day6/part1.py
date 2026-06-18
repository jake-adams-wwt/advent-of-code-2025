def readLines(filename):
    with open(filename, "r") as f:
        # Read lines WITHOUT stripping so column positions are preserved
        return [line.rstrip("\n") for line in f.readlines()]


def findProblemBoundaries(lines):
    """Return a list of (start_col, end_col) ranges, one per problem.

    Problems are separated by columns that are entirely spaces across every
    row (including the operator row at the bottom).
    """
    if not lines:
        return []

    # Pad all lines to the same width so column indexing is safe
    maxWidth = max(len(line) for line in lines)
    paddedLines = [line.ljust(maxWidth) for line in lines]

    boundaries = []
    inProblem = False
    start = 0

    for col in range(maxWidth):
        colChars = [paddedLines[row][col] for row in range(len(paddedLines))]
        isBlankCol = all(ch == " " for ch in colChars)

        if not isBlankCol and not inProblem:
            # Start of a new problem
            inProblem = True
            start = col
        elif isBlankCol and inProblem:
            # End of the current problem
            inProblem = False
            boundaries.append((start, col))

    # Handle a problem that runs to the very end of the line
    if inProblem:
        boundaries.append((start, maxWidth))

    return boundaries


def extractProblem(lines, startCol, endCol):
    """Extract numbers and operator from a vertical problem column slice.

    The last line contains the operator (* or +).
    All preceding lines contain (possibly space-padded) integers.
    """
    numbers = []
    operator = None

    for rowIndex, line in enumerate(lines):
        # Pad line if it is shorter than endCol
        paddedLine = line.ljust(endCol)
        segment = paddedLine[startCol:endCol].strip()

        isLastRow = rowIndex == len(lines) - 1

        if isLastRow:
            # The operator row — grab the first non-space character
            operator = segment.strip() if segment.strip() in ("*", "+") else None
        else:
            if segment:  # skip blank rows (shouldn't happen, but be safe)
                numbers.append(int(segment))

    return numbers, operator


def calculateResult(numbers, operator):
    """Apply the operator left-to-right across all numbers."""
    if not numbers:
        return 0

    result = numbers[0]
    for number in numbers[1:]:
        if operator == "*":
            result *= number
        elif operator == "+":
            result += number

    return result


def findAnswer(filename):
    lines = readLines(filename)

    # Drop any trailing completely-blank lines so they don't confuse parsing
    while lines and lines[-1].strip() == "":
        lines.pop()

    boundaries = findProblemBoundaries(lines)
    print(f"Found {len(boundaries)} problems in {filename}")

    grandTotal = 0

    for startCol, endCol in boundaries:
        numbers, operator = extractProblem(lines, startCol, endCol)
        result = calculateResult(numbers, operator)
        print(f"  Numbers: {numbers}, Operator: {operator}, Result: {result}")
        grandTotal += result

    return grandTotal


# --- Test ---
testAnswer = findAnswer("test.txt")
print(f"Test answer: {testAnswer}")
assert testAnswer == 4277556, f"Expected 4277556 but got {testAnswer}"

# --- Real input ---
answer = findAnswer("input.txt")
print(f"Answer: {answer}")
