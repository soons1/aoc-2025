def solve():
    adj_list = {}
    with open('input11.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            node, neighbors = line.split(":")
            neighbors = neighbors.strip().split(" ")
            adj_list[node] = neighbors

    memo = {}

    def count_constrained_paths(u, v_dac, v_fft):
        state = (u, v_dac, v_fft)
        if state in memo:
            return memo[state]
        
        new_dac = v_dac or (u == "dac")
        new_fft = v_fft or (u == "fft")
        
        if u == "out":
            return 1 if (new_dac and new_fft) else 0
        
        if u not in adj_list:
            return 0
        
        total = 0
        for neighbor in adj_list[u]:
            total += count_constrained_paths(neighbor, new_dac, new_fft)
        
        memo[state] = total
        return total

    memo_p1 = {}
    def count_paths(u):
        if u == "out": return 1
        if u in memo_p1: return memo_p1[u]
        if u not in adj_list: return 0
        total = 0
        for neighbor in adj_list[u]:
            total += count_paths(neighbor)
        memo_p1[u] = total
        return total

    result1 = count_paths("you")
    print("part 1:", result1)

    result2 = count_constrained_paths("svr", False, False)
    print("part 2:", result2)

solve()