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

    # Find problem boundaries by locating columns that are all spaces
    # A "separator" column has only spaces across all rows
    def isBlankCol(col):
        return all(lines[row][col] == ' ' for row in range(numRows))

    # Group columns into problem blocks (sequences of non-blank columns)
    problems = []
    col = 0
    while col < numCols:
        if isBlankCol(col):
            col += 1
            continue

        # Start of a new problem block
        startCol = col
        while col < numCols and not isBlankCol(col):
            col += 1
        endCol = col  # exclusive

        # Extract the text block for this problem
        block = [lines[row][startCol:endCol].strip() for row in range(numRows)]

        # Last row is the operator
        operator = block[-1].strip()
        # All other rows are numbers (skip empty strings)
        numbers = [int(b) for b in block[:-1] if b.strip() != '']

        if numbers and operator in ('+', '*'):
            problems.append((operator, numbers))

    return problems


def solveProblems(problems):
    total = 0
    for operator, numbers in problems:
        if operator == '+':
            result = sum(numbers)
        else:  # '*'
            result = 1
            for n in numbers:
                result *= n
        print(f"  {f' {operator} '.join(str(n) for n in numbers)} = {result}")
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
assert testAnswer == 4277556, f"Expected 4277556 but got {testAnswer}"

answer = findAnswer("input.txt")
print(f"Answer: {answer}")
