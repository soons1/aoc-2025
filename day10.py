import re

def solve():
    total_presses = 0
    with open('/Users/soonwei/Desktop/aoc/input10.txt', 'r') as f:
        lines = f.readlines()
    
    processed_count = 0
    for line in lines:
        line = line.strip()
        
        target_match = re.search(r'\[([.#]+)\]', line)
        target_str = target_match.group(1)
        target = 0
        for i, char in enumerate(target_str):
            if char == '#':
                target |= (1 << i)
        
        buttons_raw = re.findall(r'\(([\d,]+)\)', line)
        buttons = []
        for b_raw in buttons_raw:
            indices = map(int, b_raw.split(','))
            b_mask = 0
            for idx in indices:
                b_mask |= (1 << idx)
            buttons.append(b_mask)
        
        n_buttons = len(buttons)
        min_p = float('inf')
        
        for i in range(1 << n_buttons):
            current_mask = 0
            count = 0
            for j in range(n_buttons):
                if (i >> j) & 1:
                    current_mask ^= buttons[j]
                    count += 1
            
            if current_mask == target:
                if count < min_p:
                    min_p = count
        
        total_presses += min_p
        
        processed_count += 1
        
    print(f"part 1: {total_presses}")

solve()
