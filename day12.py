def parse_input():
    with open('input12.txt', 'r') as f:
        content = f.read()
    
    parts = content.split('\n\n')
    

    shapes_raw = []
    regions_raw = []
    
    parsing_shapes = True
    for part in parts:
        if not part.strip():
            continue
        lines = part.strip().split('\n')
        if any('x' in line and ':' in line for line in lines):
            parsing_shapes = False
            
        if parsing_shapes:
            shapes_raw.append(part)
        else:
            regions_raw.extend(lines)
            
    shapes = {}
    for raw in shapes_raw:
        lines = raw.strip().split('\n')
        if ':' in lines[0]:
            idx_str = lines[0].strip(':')
            idx = int(idx_str)
            grid = lines[1:]
            coords = set()
            for r, row in enumerate(grid):
                for c, char in enumerate(row):
                    if char == '#':
                        coords.add((r, c))
            shapes[idx] = Shape(idx, coords)
        
    regions = []
    for line in regions_raw:
        if not line.strip(): continue
        dims, counts_str = line.split(':')
        w, h = map(int, dims.split('x'))
        counts = list(map(int, counts_str.strip().split()))
        regions.append({
            'width': w,
            'height': h,
            'counts': counts,
            'original_line': line
        })

    return shapes, regions

class Shape:
    def __init__(self, idx, coords):
        self.idx = idx
        self.coords = frozenset(coords) # Fundamental shape
        self.orientations = self._generate_orientations()
        
    def _generate_orientations(self):
        base_coords = list(self.coords)
        all_variants = set()
        
        operations = [
            lambda r, c: (r, c),
            lambda r, c: (c, -r),
            lambda r, c: (-r, -c),
            lambda r, c: (-c, r),
            lambda r, c: (r, -c),
            lambda r, c: (-c, -r),
            lambda r, c: (-r, c),
            lambda r, c: (c, r),
        ]
        
        unique_orientations = []
        
        for op in operations:
            transformed = []
            min_r, min_c = float('inf'), float('inf')
            
            for r, c in base_coords:
                nr, nc = op(r, c)
                transformed.append((nr, nc))
                min_r = min(min_r, nr)
                min_c = min(min_c, nc)
            
            normalized = frozenset((r - min_r, c - min_c) for r, c in transformed)
            
            if normalized not in all_variants:
                all_variants.add(normalized)
                if not normalized: 
                    width, height = 0, 0
                else:
                    height = max(r for r, c in normalized) + 1
                    width = max(c for r, c in normalized) + 1
                    
                unique_orientations.append({
                    'coords': normalized,
                    'height': height,
                    'width': width
                })
                
        final_orientations = []
        for orient in unique_orientations:
            coords = orient['coords']
            sorted_cells = sorted(list(coords))
            first_cell = sorted_cells[0]
            
            shifted = frozenset((r - first_cell[0], c - first_cell[1]) for r, c in coords)
            final_orientations.append({
                'coords': shifted,
                'max_r': max(r for r, c in shifted),
                'max_c': max(c for r, c in shifted),
                'min_c': min(c for r, c in shifted)
            })
            
        return final_orientations

def solve_region(region, shapes):
    width = region['width']
    height = region['height']
    counts = region['counts']
    
    total_area = 0
    piece_list = []
    for idx, count in enumerate(counts):
        if idx not in shapes: 
            if count > 0: return False
            continue
        shape_area = len(shapes[idx].coords)
        total_area += shape_area * count
        for _ in range(count):
            piece_list.append(idx)
            
    if total_area > width * height:
        return False
        
    
    shape_areas_map = {idx: len(shapes[idx].coords) for idx in shapes}
    all_areas = [shape_areas_map[idx] for idx in counts if idx in shapes for _ in range(counts[idx])]
    min_piece_area = min(all_areas) if all_areas else 0
    unique_areas = set(all_areas)
    common_area = unique_areas.pop() if len(unique_areas) == 1 else None
    
    sorted_shape_ids = sorted(shapes.keys(), key=lambda k: len(shapes[k].coords), reverse=True)
    
    normalized_shapes = {}
    for s_id in sorted_shape_ids:
        s = shapes[s_id]
        new_orients = []
        for orient in s.orientations:
            sorted_cells = sorted(list(orient['coords']))
            fr, fc = sorted_cells[0]
            new_coords = frozenset((r-fr, c-fc) for r, c in orient['coords'])
            new_orients.append({
                'coords': new_coords,
            })
        normalized_shapes[s_id] = new_orients

    piece_counts = list(counts)

    grid = [False] * (width * height)
    
    max_slack = (width * height) - total_area

    def get_first_empty(start_idx):
        for i in range(start_idx, len(grid)):
            if not grid[i]:
                return i
        return -1

    def can_place(r, c, coords):
        for dr, dc in coords:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < height and 0 <= nc < width):
                return False
            if grid[nr * width + nc]:
                return False
        return True
        
    def place(r, c, coords, val):
        for dr, dc in coords:
            nr, nc = r + dr, c + dc
            grid[nr * width + nc] = val

    def flood_fill_check(min_area):
        visited = [False] * len(grid)
        for i in range(len(grid)):
            if grid[i]: visited[i] = True
        
        for i in range(len(grid)):
            if not visited[i]:
                stack = [i]
                visited[i] = True
                count = 0
                while stack:
                    curr = stack.pop()
                    count += 1
                    curr_r, curr_c = divmod(curr, width)
                    for nr, nc in [(curr_r+1, curr_c), (curr_r-1, curr_c), (curr_r, curr_c+1), (curr_r, curr_c-1)]:
                        if 0 <= nr < height and 0 <= nc < width:
                            nidx = nr * width + nc
                            if not visited[nidx]:
                                visited[nidx] = True
                                stack.append(nidx)
                
                if count < min_area:
                    return False
                if common_area and count % common_area != 0:
                    return False
        return True

    def backtrack(placed_count, total_pieces, current_counts, start_idx, current_slack):
        idx = get_first_empty(start_idx)
        
        if idx == -1:
            return placed_count == total_pieces
            
        remaining_area = 0
        rem_pieces_min = []
        for s_idx in sorted_shape_ids:
            c = current_counts[s_idx]
            if c > 0:
                area = shape_areas_map[s_idx]
                remaining_area += area * c
                rem_pieces_min.append(area)
        
        curr_min = min(rem_pieces_min) if rem_pieces_min else 0
        if not flood_fill_check(curr_min):
            return False

        r, c = divmod(idx, width)
        
        for s_id in sorted_shape_ids:
            if current_counts[s_id] > 0:
                for orient in normalized_shapes[s_id]:
                    coords = orient['coords']
                    if can_place(r, c, coords):
                        place(r, c, coords, True)
                        current_counts[s_id] -= 1
                        
                        if backtrack(placed_count + 1, total_pieces, current_counts, idx + 1, current_slack):
                            return True
                            
                        current_counts[s_id] += 1
                        place(r, c, coords, False)

        if current_slack < max_slack:
            grid[idx] = True
            if backtrack(placed_count, total_pieces, current_counts, idx + 1, current_slack + 1):
                return True
            grid[idx] = False
            
        return False
        
    return backtrack(0, len(piece_list), piece_counts, 0, 0)

def solve():
    shapes, regions = parse_input()
    
    solvable_count = 0
    for r in regions:
        area = 0
        for idx in range(len(r['counts'])):
            count = r['counts'][idx]
            if count > 0 and idx in shapes:
                area += len(shapes[idx].coords) * count
        
        cap = r['width'] * r['height']
        if area <= cap:
            solvable_count += 1
            
    print(f"part 1: {solvable_count}")

solve()
