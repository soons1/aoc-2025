def solve():
    with open('input2.txt', 'r') as file:
    for line in file:
        ranges = line.split(",")

    count = 0
            
    for r in ranges:
        two_ends = r.split("-")
        start = int(two_ends[0])
        end = int(two_ends[1])
        for i in range(start, end + 1):
            str_i = str(i)
            length = len(str_i)
            
            if length % 2 == 0:
                half_n = length // 2
                if str_i[:half_n] == str_i[half_n:]:
                    count += i

    print("part 1: " + str(count))

    with open('input2.txt', 'r') as file:
        for line in file:
            ranges = line.split(",")

    count = 0
            
    for r in ranges:
        two_ends = r.split("-")
        start = int(two_ends[0])
        end = int(two_ends[1])
        for i in range(start, end + 1):
            str_i = str(i)
            length = len(str_i)
            
            for k in range(1, length // 2 + 1):
                if length % k == 0:
                    pattern = str_i[:k]
                    times = length // k
                    if pattern * times == str_i:
                        count += i
                        break


    print("part 2: " + str(count))

solve()