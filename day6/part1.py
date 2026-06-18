def parse_worksheet(lines):
    """
    Parse the worksheet to extract individual problems.
    Each problem consists of numbers arranged vertically with an operation at the bottom.
    Problems are separated by columns of spaces.
    """
    # Read all lines and strip trailing whitespace
    lines = [line.rstrip('\n') for line in lines]
    
    if len(lines) < 2:
        return []
    
    # The first line contains numbers, the second line contains operations
    numbers_line = lines[0]
    operations_line = lines[1]
    
    # Pad operations line to match numbers line length
    operations_line = operations_line.ljust(len(numbers_line))
    
    problems = []
    current_problem = {'numbers': [], 'operation': None}
    in_problem = False
    
    col = 0
    while col < len(numbers_line):
        char = numbers_line[col]
        op_char = operations_line[col] if col < len(operations_line) else ' '
        
        # Check if this is a space column (problem separator)
        if char == ' ' and op_char == ' ':
            if in_problem:
                # End of current problem
                if current_problem['numbers']:
                    problems.append(current_problem)
                current_problem = {'numbers': [], 'operation': None}
                in_problem = False
            col += 1
        else:
            # Part of a problem
            in_problem = True
            
            # Extract the number at this column
            if char.isdigit():
                num_str = ''
                temp_col = col
                while temp_col < len(numbers_line) and numbers_line[temp_col].isdigit():
                    num_str += numbers_line[temp_col]
                    temp_col += 1
                current_problem['numbers'].append(int(num_str))
                col = temp_col
            else:
                col += 1
            
            # Extract the operation at this column
            if op_char in ['+', '*']:
                current_problem['operation'] = op_char
    
    # Don't forget the last problem
    if current_problem['numbers']:
        problems.append(current_problem)
    
    return problems


def solve_problem(numbers, operation):
    """
    Solve a single problem by applying the operation to all numbers.
    """
    if not numbers:
        return 0
    
    result = numbers[0]
    for num in numbers[1:]:
        if operation == '+':
            result += num
        elif operation == '*':
            result *= num
    
    return result


# Read the input file
with open("input.txt", "r") as f:
    lines = f.readlines()

# Parse the worksheet
problems = parse_worksheet(lines)

# Solve each problem and sum the results
grand_total = 0
for problem in problems:
    answer = solve_problem(problem['numbers'], problem['operation'])
    grand_total += answer
    print(f"Problem: {problem['numbers']} {problem['operation']} = {answer}")

print(f"\nGrand total: {grand_total}")
