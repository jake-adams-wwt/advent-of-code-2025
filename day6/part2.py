# Part 2 - placeholder until Part 2 problem description is available

def readFile(filename):
    with open(filename, "r") as f:
        # Read lines but do NOT strip, to preserve column alignment
        return [line.rstrip('\n') for line in f.readlines()]


def parseProblems(lines):
    """
    The worksheet is laid out horizontally:
    - Each problem's numbers are stacked vertically in columns
    - Problems are separated by a full column of spaces
    - The last row contains the operator (+ or *) for each problem
    """
    if not lines:
        return []

    # Make all lines the same length by padding with spaces
    maxLen = max(len(line) for line in lines)
    lines = [line.ljust(maxLen) for line in lines]

    numRows = len(lines)
    numCols = maxLen

    def isBlankCol(col):
        return all(lines[row][col] == ' ' for row in range(numRows))

    problems = []
    col = 0
    while col < numCols:
        if isBlankCol(col):
            col += 1
            continue

        startCol = col
        while col < numCols and not isBlankCol(col):
            col += 1
        endCol = col

        block = [lines[row][startCol:endCol].strip() for row in range(numRows)]

        operator = block[-1].strip()
        numbers = [int(b) for b in block[:-1] if b.strip() != '']

        if numbers and operator in ('+', '*'):
            problems.append((operator, numbers))

    return problems


def solveProblems(problems):
    total = 0
    for operator, numbers in problems:
        if operator == '+':
            result = sum(numbers)
        else:
            result = 1
            for n in numbers:
                result *= n
        total += result
    return total


def findAnswer(fileName):
    lines = readFile(fileName)
    problems = parseProblems(lines)
    print(f"Found {len(problems)} problems:")
    total = solveProblems(problems)
    return total


testAnswer = findAnswer("test-input.txt")
print(f"Test answer: {testAnswer}")

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
