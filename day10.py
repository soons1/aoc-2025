import re
from fractions import Fraction

def solve():
    with open('input10.txt', 'r') as f:
        lines = f.readlines()
    
    # Part 1
    total_presses_p1 = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        
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
        if min_p != float('inf'):
            total_presses_p1 += min_p
    print(f"part 1: {total_presses_p1}")

    # Part 2
    total_presses_p2 = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        buttons_raw = re.findall(r'\(([\d,]+)\)', line)
        buttons = []
        for b_raw in buttons_raw:
            indices = set(map(int, b_raw.split(',')))
            buttons.append(indices)
        
        req_match = re.search(r'\{([\d,]+)\}', line)
        requirements = list(map(int, req_match.group(1).split(',')))
        
        res, n_free = solve_machine_part2(buttons, requirements)
        total_presses_p2 += res
    print(f"part 2: {total_presses_p2}")

def solve_machine_part2(buttons, requirements):
    n_btns = len(buttons)
    n_counters = len(requirements)
    
    matrix = []
    for c_idx in range(n_counters):
        row = [0] * n_btns + [requirements[c_idx]]
        for b_idx, b_set in enumerate(buttons):
            if c_idx in b_set:
                row[b_idx] = 1
        matrix.append([Fraction(x) for x in row])
        
    pivot_row = 0
    pivot_cols = []
    for j in range(n_btns):
        if pivot_row >= n_counters: break
        for i in range(pivot_row, n_counters):
            if matrix[i][j] != 0:
                matrix[pivot_row], matrix[i] = matrix[i], matrix[pivot_row]
                break
        else: continue
        
        pivot_val = matrix[pivot_row][j]
        for k in range(j, n_btns + 1):
            matrix[pivot_row][k] /= pivot_val
        for i in range(n_counters):
            if i != pivot_row and matrix[i][j] != 0:
                factor = matrix[i][j]
                for k in range(j, n_btns + 1):
                    matrix[i][k] -= factor * matrix[pivot_row][k]
        pivot_cols.append(j)
        pivot_row += 1
        
    for i in range(pivot_row, n_counters):
        if matrix[i][n_btns] != 0: return 0, 0 # Inconsistent

    free_cols = [j for j in range(n_btns) if j not in pivot_cols]
    
    # print(f"  Rank: {len(pivot_cols)}, Free: {len(free_cols)}")
    
    # X[pivot_i] = Target_i - sum(Coeff_ij * X_free_j)
    pivot_exprs = []
    for i in range(len(pivot_cols)):
        coeffs = []
        for j, f_col in enumerate(free_cols):
            if matrix[i][f_col] != 0:
                coeffs.append((j, matrix[i][f_col]))
        pivot_exprs.append((matrix[i][n_btns], coeffs))

    # Bounds for each free variable
    # X_f <= min(R_k) for all k affected by X_f
    free_bounds = []
    for f_col in free_cols:
        limit = float('inf')
        for c_idx in range(n_counters):
            if c_idx in buttons[f_col]:
                limit = min(limit, requirements[c_idx])
        if limit == float('inf'): limit = 500
        free_bounds.append(int(limit))

    best_sum = float('inf')
    
    def search_free(idx, current_vals):
        nonlocal best_sum
        if sum(current_vals) >= best_sum:
            return
        
        if idx == len(free_cols):
            current_sum = sum(current_vals)
            for target_val, coeffs in pivot_exprs:
                v = target_val
                for f_idx, coeff in coeffs:
                    v -= coeff * current_vals[f_idx]
                if v < 0 or v.denominator != 1: return
                current_sum += int(v)
            if current_sum < best_sum:
                best_sum = current_sum
            return

        for val in range(free_bounds[idx] + 1):
            # Optimization: check if any pivot variable is already forced to be negative
            early_fail = False
            # Check all pivot exprs that only depend on already fixed free variables
            # Actually, just check if target_val - sum(coeffs * val) < some min possible
            # But let's keep it simple first.
            search_free(idx + 1, current_vals + [val])

    search_free(0, [])
    return (int(best_sum) if best_sum != float('inf') else 0), len(free_cols)

if __name__ == "__main__":
    solve()
