import heapq

def dijkstra(start, end, maze):
    """
    Simple Dijkstra for a 4-connected grid.
    maze: 2D sequence where 0 = blocked, 1 = open, 'S'/'E' allowed
    start, end: (row, col) tuples
    Returns list of (row,col) from start to end or None if unreachable.
    """
    rows, cols = len(maze), len(maze[0])
    visited = set()
    pq = []
    heapq.heappush(pq, (0, start))
    parents = {start: None}

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            # reconstruct path
            path = []
            cur = node
            while cur is not None:
                path.append(cur)
                cur = parents[cur]
            path.reverse()
            return path
        r, c = node
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                val = maze[nr][nc]
                if val in (1, 'E', 'S'):
                    neigh = (nr, nc)
                    if neigh in visited:
                        continue
                    if neigh not in parents:
                        parents[neigh] = node
                        heapq.heappush(pq, (cost + 1, neigh))
    return None


