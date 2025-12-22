def solve():
    count = 0
    start = 50

    with open('input1.txt', 'r') as file:
        for line in file:
            number = int(line[1:])
            if line[0] == "L":
                start -= number
            else:
                start += number
                    
            if start % 100 == 0:
                count += 1

    print("part 1: " + str(count))

    count = 0
    start = 50

    with open('input1.txt', 'r') as file:
        for line in file:
            number = int(line[1:])
            count += abs(number) // 100
            if line[0] == "L":
                a = -1
            else:
                a = 1
            rem = a * (number % 100)
            start += rem
            if start >= 100 or (start <= 0 and start != rem):
                count += 1
            start %= 100

        print("part 2: " + str(count))

solve()