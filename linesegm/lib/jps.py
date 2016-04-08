

def identify_successors(grid, node, parent, open, close, parents, goal):
    if str(node) in parents:
        parent = parents[str(node)]
    else:
        parent = None

    neighbors = find_neighbors(grid, node, parent)

    for neighbor in neighbors:
        jump_node = jump(grid, node, neighbor, goal)

        if str(jump_node) in close:
            continue
        # not implemented yet, just a scheme
        new_gscore = gscore + compute_cost()
        if jump_node not in parents and new_gscore < gscore:
            gscore = new_gscore
            fscore = new_gscore + heuristic()
            open.put(jump_node, fscore)
            parent[str(jump_node)] = node

def jump(grid, node, neighbor, goal):
    pass


def find_neighbors(grid, node, parent):
    if parent:
        # get neighbors based on direction
        neighbors = []
        r, c = node
        dr, dc = direction(node, parent)

        # Diagonal direction
        if dr != 0 and dc != 0:
            neighbors.append([r, c + dc])
            neighbors.append([r + dr, c])
            neighbors.append([r + dr, c + dc])
            # forced neighbors
            if wall(grid, [r, c - dc]):
                neighbors.append([r + dr, c - dc])
            if wall(grid, [r - dr, c]):
                neighbors.append([r - dr, c + dc])
        # Columns direction
        elif dc != 0:
            neighbors.append([r, c + dc])
            # forced neighbors
            if wall(grid, [r + 1, c]):
                neighbors.append([r + 1, c + dc])
            if wall(grid, [r - 1, c]):
                neighbors.append([r - 1, c + dc])
        # Rows direction
        elif dr != 0:
            neighbors.append([r + dr, c])
            # forced neighbors
            if wall(grid, [r,  c + dc]):
                neighbors.append([r + dr, c + dc])
            if wall(grid, [r, c - dc]):
                neighbors.append([r + dr, c - dc])

        return neighbors
    else:
        # does not have a parent, return all the neighbors
        return get_neighbors(grid, node)


def direction(node, parent):
    dr = (node[0] - parent[0])/max(abs(node[0] - parent[0]), 1)
    dc = (node[1] - parent[1])/max(abs(node[1] - parent[1]), 1)

    return dr, dc


def wall(grid, node):
    r, c = node
    if grid[r, c] == 0:
        return True
    else:
        return False


def get_neighbors(grid, node):
    r, c = node
    s = 1
    neighbors = [[r - s, c - s], [r - s, c], [r - s, c + s],
                 [r, c - s], [r, c + s],
                 [r + s, c - s], [r + s, c], [r + s, c + s]]
    return filter(lambda x: in_bounds(grid, x), neighbors)


def in_bounds(grid, node):
    (r, c) = node
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]
