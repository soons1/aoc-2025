def solve():
    sum = 0
    with open('input3.txt', 'r') as file:
            for line in file:
                line = line.strip()

                for i in range(9, -1, -1):
                    d1 = str(i)
                    idx = line.find(d1)
                    
                    if idx != -1 and idx < len(line) - 1:
                        remaining = line[idx+1:]
                        d2 = max(remaining)
                        sum += (i * 10 + int(d2))
                        break
    print("part 1: " + str(sum))

    sum = 0
    with open('input3.txt', 'r') as file:
        for line in file:
            line = line.strip()
            res = ""
            search_start = 0
            digits_needed = 12
            while digits_needed > 0:    
                search_end = len(line) - digits_needed + 1
                remaining_window = line[search_start:search_end]
                max_d = max(remaining_window)
                idx_in_window = remaining_window.find(max_d)
                res += max_d
                search_start += idx_in_window + 1
                digits_needed -= 1
            
            sum += int(res)

    print("part 2: " + str(sum))

solve()
