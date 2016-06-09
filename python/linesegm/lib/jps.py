from lib import astar


class Jps:

    def __init__(self, grid):
        self.finder = astar.Astar(grid)

    def pathfind(self, start, goal):
        self.start = start
        self.goal = goal
        self.finder.gscore[tuple(self.start)] = 0
        self.finder.open.put(self.start, self.finder.heuristic(self.start, self.goal))

        print 'start: ' + str(self.start) + " - goal: " + str(self.goal),

        while not self.finder.open.empty():
            current = self.finder.open.get()
            # print 'current: ' + str(current)
            # print current, self.finder.gscore[tuple(current)], self.finder.open.size()
            self.finder.close.append(current)

            if current == self.goal:
                return self.reconstruct_path(current)

            self.identify_successors(current)

        return None

    def identify_successors(self, node):
        neighbors = self.find_neighbors(node)
        # print 'neighbors: ' + str(neighbors)

        for neighbor in neighbors:
            # print '----------'
            jump_node = self.jump(neighbor, node)
            # print 'jump_node: ' + str(jump_node)
            if not jump_node:
                continue

            if jump_node in self.finder.close:
                continue

            # new_gscore = self.finder.gscore[tuple(node)] + self.finder.compute_cost(node, jump_node, self.start)
            new_gscore = self.finder.gscore[tuple(node)] + self.finder.heuristic(node, jump_node)
            if jump_node not in self.finder.close or new_gscore < self.finder.get_gscore(tuple(jump_node)):
                self.finder.gscore[tuple(jump_node)] = new_gscore
                self.finder.parents[str(jump_node)] = node
                fscore = new_gscore + self.finder.heuristic(jump_node, self.goal)
                self.finder.open.put(jump_node, fscore)

    def jump(self, node, parent):
        while(True):

            if not self.finder.walkable(node):
                return None
            elif node == self.goal:
                return node

            r, c = node
            pr, pc = parent
            dr, dc = r - pr, c - pc

            if dr != 0 and dc != 0:
                if (self.finder.walkable([r - dr, c + dc]) and not self.finder.walkable([r - dr, c]) or
                        self.finder.walkable([r + dr, c - dc]) and not self.finder.walkable([r, c - dc])):
                    return node
            else:
                if dr != 0:
                    if (self.finder.walkable([r + dr, c + 1]) and not self.finder.walkable([r, c + 1]) or
                            self.finder.walkable([r + dr, c - 1]) and not self.finder.walkable([r, c - 1])):
                        return node
                # Horizontal case
                else:
                    if (self.finder.walkable([r + 1, c + dc]) and not self.finder.walkable([r + 1, c]) or
                            self.finder.walkable([r - 1, c + dc]) and not self.finder.walkable([r - 1, c])):
                        return node

            if dr != 0 and dc != 0:
                if self.jump([r + dr, c], node) or self.jump([r, c + dc], node):
                    return node

            parent = node
            node = [r + dr, c + dc]

    def jump_old(self, node, parent):
        if not node:
            return None

        r, c = node
        pr, pc = parent
        dr, dc = r - pr, c - pc

        if not self.finder.walkable(node):
            return None

        # print node, parent, dr, dc

        if node == self.goal:
            return node
        # Diagonal case
        if dr != 0 and dc != 0:
            if (self.finder.walkable([r - dr, c + dc]) and not self.finder.walkable([r - dr, c]) or
                    self.finder.walkable([r + dr, c - dc]) and not self.finder.walkable([r, c - dc])):
                return node
        # Vertical case
        elif dr != 0:
            if (self.finder.walkable([r + dr, c + 1]) and not self.finder.walkable([r, c + 1]) or
                    self.finder.walkable([r + dr, c - 1]) and not self.finder.walkable([r, c - 1])):
                return node
        # Horizontal case
        elif dc != 0:
            if (self.finder.walkable([r + 1, c + dc]) and not self.finder.walkable([r + 1, c]) or
                    self.finder.walkable([r - 1, c + dc]) and not self.finder.walkable([r - 1, c])):
                return node
        # Recursive horizontal/vertical search
        if dr != 0 and dc != 0:
            if self.jump([r + dr, c], node):
                return node
            if self.jump([r, c + dc], node):
                return node
        # Recursive diagonal search
        if self.finder.walkable([r + dr, c]) or self.finder.walkable([r, c + dc]):
            return self.jump([r + dr, c + dc], node)

    def find_neighbors(self, node):

        if str(node) in self.finder.parents:
            neighbors = []

            r, c = node
            dr, dc = self.direction(node, self.finder.parents[str(node)])

            # Diagonal case
            if dr != 0 and dc != 0:
                walkR, walkC = False, False
                # Natural neighbors
                if self.finder.walkable([r, c + dc]):
                    neighbors.append([r, c + dc])
                    walkC = True
                if self.finder.walkable([r + dr, c]):
                    neighbors.append([r + dr, c])
                    walkR = True
                if walkC and walkR:
                    neighbors.append([r + dr, c + dc])
                # Forced neighbors
                if (not self.finder.walkable([r - dr, c])) and walkC:
                    neighbors.append([r - dr, c + dr])
                if (not self.finder.walkable([r, c - dc])) and walkR:
                    neighbors.append([r + dr, c - dc])
            # Horizontal case
            elif dc != 0:
                if self.finder.walkable([r, c + dc]):
                    neighbors.append([r, c + dc])
                # Forced neighbors
                if not self.finder.walkable([r + 1, c]):
                    neighbors.append([r + 1, c + dc])
                if not self.finder.walkable([r - 1, c]):
                    neighbors.append([r - 1, c + dc])
            # Vertical case
            elif dr != 0:
                if self.finder.walkable([r + dr, c]):
                    neighbors.append([r + dr, c])
                # Forced neighbors
                if not self.finder.walkable([r, c + 1]):
                    neighbors.append([r + dr, c + 1])
                if not self.finder.walkable([r, c - 1]):
                    neighbors.append([r + dr, c - 1])

            return neighbors
        else:
            return self.finder.get_neighbors(node)

    def get_neighbors(self, node):
        r, c = node
        return [[r, c + 1]]

    def direction(self, node, parent):
        dr = (node[0] - parent[0])/max(abs(node[0] - parent[0]), 1)
        dc = (node[1] - parent[1])/max(abs(node[1] - parent[1]), 1)

        return dr, dc

    def reconstruct_path(self, current):
        total_path = [current]
        while str(current) in self.finder.parents:
            parent = self.finder.parents[str(current)]
            r, c = current
            dr, dc = self.direction(parent, current)
            tmp = [r, c]
            while tmp != parent:
                r += dr
                c += dc
                tmp = [r, c]
                total_path.append(tmp)

            current = parent
            total_path.append(current)

        return total_path, self.finder.close
