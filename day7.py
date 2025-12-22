from collections import Counter

def solve():
    grid = []
    split_count = 0
    pointer_lst = set()

    with open('input7.txt', 'r') as file:
        for line in file:
            line_lst = list(line.strip())
            if 'S' in line_lst:
                pointer_lst.add(line_lst.index('S'))
            grid.append(line_lst)

    for i in range(len(grid) - 1):
        tmp = set()
        for beam in pointer_lst:
            if grid[i + 1][beam] == '^':
                tmp.add(beam - 1)
                tmp.add(beam + 1)
                split_count += 1
            else:
                tmp.add(beam)
        pointer_lst = tmp

    print("part 1:", split_count)

    grid = []

    with open('input7.txt', 'r') as file:
        for line in file:
            line_lst = list(line.strip())
            grid.append(line_lst)

    pointer_counts = Counter()
    for x, char in enumerate(grid[0]):
        if char == 'S':
            pointer_counts[x] = 1
    for i in range(len(grid) - 1):
        next_counts = Counter()
        for beam_pos, count in pointer_counts.items():
            next_cell = grid[i + 1][beam_pos]
            
            if next_cell == '^':
                if beam_pos - 1 >= 0:
                    next_counts[beam_pos - 1] += count
                if beam_pos + 1 < len(grid[0]):
                    next_counts[beam_pos + 1] += count
            else:
                next_counts[beam_pos] += count
                
        pointer_counts = next_counts

    print("part 2:", sum(pointer_counts.values()))

solve()