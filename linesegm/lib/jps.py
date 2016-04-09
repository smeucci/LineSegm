from lib import astar


class Jps():

    def __init__(self,  grid):
        self.finder = astar.Astar(grid)

    def pathfind(self, start, goal):
        self.finder.open.put(start, self.finder.heuristic(start, goal))

    def identify_successors(self, node):
        if str(node) in self.parents:
            parent = self.parents[str(node)]
        else:
            parent = None

        neighbors = self.find_neighbors(node, parent)

        for neighbor in neighbors:
            jump_node = self.jump(node, neighbor)

            if jump_node in self.close:
                continue

            new_gscore = self.gscore[tuple(node)] + self.compute_cost(node, neighbor)

            if (str(jump_node) not in self.parents or new_gscore < self.get_gscore(tuple(jump_node))):
                self.gscore[tuple(jump_node)] = new_gscore
                fscore = new_gscore + self.heuristic(jump_node, self.goal)
                self.open.put(jump_node, fscore)
                self.parents[str(jump_node)] = node

    def jump(self, node, neighbor, goal):
        pass

    def find_neighbors(self, node, parent):
        if parent:
            # get neighbors based on direction
            neighbors = []
            r, c = node
            dr, dc = self.direction(node, parent)

            # Diagonal direction
            if dr != 0 and dc != 0:
                neighbors.append([r, c + dc])
                neighbors.append([r + dr, c])
                neighbors.append([r + dr, c + dc])
                # forced neighbors
                if self.wall([r, c - dc]):
                    neighbors.append([r + dr, c - dc])
                if self.wall([r - dr, c]):
                    neighbors.append([r - dr, c + dc])
            # Columns direction
            elif dc != 0:
                neighbors.append([r, c + dc])
                # forced neighbors
                if self.wall([r + 1, c]):
                    neighbors.append([r + 1, c + dc])
                if self.wall([r - 1, c]):
                    neighbors.append([r - 1, c + dc])
            # Rows direction
            elif dr != 0:
                neighbors.append([r + dr, c])
                # forced neighbors
                if self.wall([r,  c + dc]):
                    neighbors.append([r + dr, c + dc])
                if self.wall([r, c - dc]):
                    neighbors.append([r + dr, c - dc])

            return neighbors
        else:
            # does not have a parent, return all the neighbors
            return self.get_neighbors(node)

    def direction(self, node, parent):
        dr = (node[0] - parent[0])/max(abs(node[0] - parent[0]), 1)
        dc = (node[1] - parent[1])/max(abs(node[1] - parent[1]), 1)

        return dr, dc

    def wall(self, node):
        r, c = node
        if self.grid[r, c] == 0:
            return True
        else:
            return False
