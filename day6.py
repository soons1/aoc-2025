def solve1():
    numbers = []
    total = 0
    with open('input6.txt', 'r') as file:
        for _ in range(4):
            line = file.readline().strip()
            number_int = [int(x) for x in line.split()]
            numbers.append(number_int)

        operations = file.readline().strip().split()

    for i in range(len(operations)):
        op = operations[i]
        var1 = numbers[0][i]
        var2 = numbers[1][i]
        var3 = numbers[2][i]
        var4 = numbers[3][i]
        if op == '+':
            total += (var1 + var2 + var3 + var4)
        else:
            total += (var1 * var2 * var3 * var4)

    print("part 1: " + str(total))

solve1()

def calculate(numbers, operator):
    if operator == '+':
        return sum(numbers)
    else:
        result = 1
        for n in numbers:
            result *= n
        return result

def solve2():
    with open('input6.txt', 'r') as file:
        lines = [line.rstrip('\n') for line in file]

    max_len = max(len(line) for line in lines)
    grid = [line.ljust(max_len) for line in lines]

    rows = len(grid)
    cols = len(grid[0])

    grand_total = 0

    current_numbers = []
    current_operator = None

    for c in range(cols - 1, -1, -1):
        col_chars = [grid[r][c] for r in range(rows)]
        
        is_empty = all(char == ' ' for char in col_chars)
        
        if is_empty:
            if current_numbers:
                result = calculate(current_numbers, current_operator)
                grand_total += result
                current_numbers = []
                current_operator = None
            continue

        bottom_char = col_chars[-1]
        
        if bottom_char in ['+', '*']:
            current_operator = bottom_char
        digit_str = "".join([char for char in col_chars[:-1] if char.isdigit()])
        
        if digit_str:
            current_numbers.append(int(digit_str))
            

    if current_numbers:
        result = calculate(current_numbers, current_operator)
        grand_total += result

    print("part 2:", grand_total)

solve2()