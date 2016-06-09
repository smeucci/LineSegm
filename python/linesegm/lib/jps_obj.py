from lib import astar_obj


class Jps():

    def __init__(self,  grid):
        self.finder = astar_obj.Astar(grid)

    def pathfind(self, start, goal):
        self.start = astar_obj.Node(start[0], start[1])
        self.goal = astar_obj.Node(goal[0], goal[1])
        self.start.gscore = 0
        self.finder.open.put(self.start, self.finder.heuristic(self.start, self.goal))

        while not self.finder.open.empty():
            current = self.finder.open.get()
            self.finder.close.append(current)

            if current == self.goal:
                return self.finder.reconstruct_path(current)

            self.identify_successors(current)

        return None

    def identify_successors(self, node):
        neighbors = self.find_neighbors(node)
        print neighbors
        for neighbor in neighbors:
            jump_node = self.jump(neighbor, node)

            if jump_node is None:
                continue

            if jump_node in self.finder.close:
                continue

            new_gscore = node.gscore + self.finder.compute_cost(node, jump_node, self.start)

            if jump_node.parent is not None or new_gscore < neighbor.gscore:
                neighbor.gscore = new_gscore
                fscore = new_gscore + self.finder.heuristic(jump_node, self.goal)
                jump_node.parent = node
                self.finder.open.put(jump_node, fscore)

    def jump(self, node, parent):
        if not node or not self.finder.in_bounds(node):
            return None

        r, c = node.row, node.col
        dr, dc = r - parent.row, c - parent.col
        print node, parent, dr, dc

        if self.wall([r, c]):
            return None

        if node == self.goal:
            return node

        # Diagonal case
        if dr != 0 and dc != 0:
            if ((not self.wall([r - dr, c - dc]) and self.wall([r, c - dc])) or
                    (not self.wall([r + dr, c + dc]) and self.wall([r + dr, c]))):
                return node
        # Horizontal case
        if dc != 0:
            if ((not self.wall([r - 1, c + dc]) and self.wall([r - 1, c])) or
                    (not self.wall([r + 1, c + dc]) and self.wall([r + 1, c]))):
                return node
        # Vertical case
        if dr != 0:
            if ((not self.wall([r - dr, c - 1]) and self.wall([r, c - 1])) or
                    (not self.wall([r - dr, c + 1]) and self.wall([r, c + 1]))):
                return node
        # Recursive horizontal/vertical search
        if dr != 0 and dc != 0:
            if self.jump(astar_obj.Node(r, c + dc), node):
                return node
            if self.jump(astar_obj.Node(r + dr, c), node):
                return node
        # Recursive diagonal search
        if not self.wall([r, c + dc]) or not self.wall([r + dr, c]):
            return self.jump(astar_obj.Node(r + dr, c + dc), node)

    def find_neighbors(self, node):
        if node.parent is not None:
            # get neighbors based on direction
            neighbors = []
            r, c = node.row, node.col
            dr, dc = self.direction(node)

            # Diagonal direction
            if dr != 0 and dc != 0:
                neighbors.append(astar_obj.Node(r, c + dc))
                neighbors.append(astar_obj.Node(r + dr, c))
                neighbors.append(astar_obj.Node(r + dr, c + dc))
                # forced neighbors
                if self.wall([r, c - dc]):
                    neighbors.append(astar_obj.Node(r + dr, c - dc))
                if self.wall([r - dr, c]):
                    neighbors.append(astar_obj.Node(r - dr, c + dc))
            # Horizontal direction
            elif dc != 0:
                neighbors.append(astar_obj.Node(r, c + dc))
                # forced neighbors
                if self.wall([r + 1, c]):
                    neighbors.append(astar_obj.Node(r + 1, c + dc))
                if self.wall([r - 1, c]):
                    neighbors.append(astar_obj.Node(r - 1, c + dc))
            # Vertical direction
            elif dr != 0:
                neighbors.append(astar_obj.Node(r + dr, c))
                # forced neighbors
                if self.wall([r,  c + dc]):
                    neighbors.append(astar_obj.Node(r + dr, c + dc))
                if self.wall([r, c - dc]):
                    neighbors.append(astar_obj.Node(r + dr, c - dc))

            return neighbors
        else:
            # does not have a parent, return all the neighbors
            return self.finder.get_neighbors(node)

    def direction(self, node):
        dr = (node.row - node.parent.row)/max(abs(node.row - node.parent.row), 1)
        dc = (node.col - node.parent.col)/max(abs(node.col - node.parent.col), 1)

        return dr, dc

    def wall(self, node):
        r, c = node
        try:
            if self.finder.grid[r, c] == 0:
                return True
            else:
                return False
        except IndexError:
            return True
