def solve():
    vertices = []
    with open('input9.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                vertices.append(list(map(int, line.split(','))))

    max_area_1 = 0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        for j in range(i + 1, n):
            x2, y2 = vertices[j]
            max_area_1 = max(max_area_1, (abs(x2 - x1) + 1) * ( abs(y2 - y1) + 1))
    
    print("part 1:", max_area_1)
    
    edges = []
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        edges.append((min(p1[0], p2[0]), max(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[1], p2[1])))

    def is_point_inside(x, y):
        inside = False
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside

    max_area_2 = 0
    
    for i in range(n):
        x1, y1 = vertices[i]
        for j in range(i + 1, n):
            x2, y2 = vertices[j]
                
            rx_min, rx_max = min(x1, x2), max(x1, x2)
            ry_min, ry_max = min(y1, y2), max(y1, y2)
            
            possible = True
            for ex_min, ex_max, ey_min, ey_max in edges:
                if ex_min == ex_max:
                    if rx_min < ex_min < rx_max:
                        if not (ey_max <= ry_min or ey_min >= ry_max):
                            possible = False
                            break
                else:
                    if ry_min < ey_min < ry_max:
                        if not (ex_max <= rx_min or ex_min >= rx_max):
                            possible = False
                            break
            
            if not possible:
                continue
                
            if is_point_inside((rx_min + rx_max) / 2, (ry_min + ry_max) / 2):
                area = (rx_max - rx_min + 1) * (ry_max - ry_min + 1)
                if area > max_area_2:
                    max_area_2 = area

    print("part 2:", max_area_2)

solve()