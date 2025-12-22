class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False

def solve():
    boxes = []
    with open('input8.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                boxes.append(list(map(int, line.split(','))))

    n = len(boxes)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist_sq = (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2
            edges.append((dist_sq, i, j))

    edges.sort()

    dsu1 = DSU(n)
    for i in range(1000):
        _, u, v = edges[i]
        dsu1.union(u, v)

    root_to_size = {}
    for i in range(n):
        root = dsu1.find(i)
        root_to_size[root] = dsu1.size[root]
    sizes = sorted(root_to_size.values(), reverse=True)
    if len(sizes) >= 3:
        print(f"part 1: {sizes[0] * sizes[1] * sizes[2]}")

    dsu2 = DSU(n)
    num_components = n
    for dist_sq, u, v in edges:
        if dsu2.union(u, v):
            num_components -= 1
            if num_components == 1:
                print(f"part 2: {boxes[u][0] * boxes[v][0]}")
                break

solve()
