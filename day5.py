def solve():
    ranges = []
    merged_ranges = []
    count = 0
    with open('input5.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                break
            
            parts = line.split('-')
            ranges.append((int(parts[0]), int(parts[1])))

        ranges.sort()
        
        if ranges:
            curr_start, curr_end = ranges[0]
            
            for i in range(1, len(ranges)):
                next_start, next_end = ranges[i]
                
                if next_start <= curr_end + 1:
                    curr_end = max(curr_end, next_end)
                else:
                    merged_ranges.append((curr_start, curr_end))
                    curr_start, curr_end = next_start, next_end
            
            merged_ranges.append((curr_start, curr_end))

        for line in file:
            number = int(line.strip())
            for start, end in merged_ranges:
                if number < start:
                    break
                if start <= number <= end:
                    count += 1
                    break

    print("part 1: " + str(count))

    fresh_count = 0

    for start, end in merged_ranges:
        fresh_count += (end - start + 1)

    print("part 2: " + str(fresh_count))

solve()