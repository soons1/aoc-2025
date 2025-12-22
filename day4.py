def solve():
    count = 0
    grid = []
    with open('input4.txt', 'r') as file:
        for line in file:
            line = line.strip()
            line_array = list(line)
            grid.append(line_array)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != '@':
                continue

            paper_count = 0

            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    
                    ni = i + di
                    nj = j + dj

                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                        if grid[ni][nj] == '@':
                            paper_count += 1
            
            if paper_count < 4:
                count += 1
            

    print("part 1: " + str(count))

    grid = []
    with open('input4.txt', 'r') as file:
        for line in file:
            line = line.strip()
            line_array = list(line)
            grid.append(line_array)

    total_count = 0

    while True:
        count_per_round = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] != '@':
                    continue

                paper_count = 0

                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        
                        ni = i + di
                        nj = j + dj

                        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                            if grid[ni][nj] == '@' or grid[ni][nj] == 'x':
                                paper_count += 1
                
                if paper_count < 4:
                    count_per_round += 1
                    grid[i][j] = 'x'

        if count_per_round == 0:
            break
        total_count += count_per_round
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'x':
                    grid[i][j] = '.'

    print("part 2: " + str(total_count))

solve()