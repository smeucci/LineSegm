import numpy as np
import heapq


class PriorityQueue():

    def __init__(self):
        self.list = []

    def empty(self):
        return len(self.list) == 0

    def put(self, item, priority):
        heapq.heappush(self.list, (priority, item))

    def get(self):
        return heapq.heappop(self.list)[1]

    def size(self):
        return len(self.list)

    def flush(self):
        size = self.size()
        [self.list.pop() for i in range(size / 2, size - 1)]
        heapq.heapify(self.list)


class Astar():

    def __init__(self):
        self.parents = {}
        self.open = PriorityQueue()
        self.close = []

    def pathfind(self, im, start, goal, step):
        # initialize
        self.grid = im / 255
        self.start = start
        self.goal = goal
        self.step = step
        self.open.put(self.start, self.heuristic(self.start, self.goal))
        self.gscore = np.zeros((self.grid.shape), dtype=np.int32)
        self.gscore[tuple(self.start)] = 0

        while not self.open.empty():

            current = self.open.get()
            # self.print_info(current)

            if current == self.goal:
                return self.reconstruct_path(current)

            self.close.append(current)

            for neighbor in self.get_neighbors(current):

                if neighbor in self.close:
                    continue

                new_gscore = self.gscore[tuple(current)] + \
                    self.compute_cost(current, neighbor)

                if (str(neighbor) not in self.parents or
                        new_gscore < self.get_gscore(tuple(neighbor))):
                    self.gscore[tuple(neighbor)] = new_gscore
                    fscore = new_gscore + self.heuristic(neighbor, self.goal)
                    self.open.put(neighbor, fscore)
                    self.parents[str(neighbor)] = current

        return None

    def heuristic(self, current, goal):
        # return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return 20*((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    def get_neighbors(self, node):
        r, c = node
        s = self.step
        neighbors = [[r - s, c - s], [r - s, c], [r - s, c + s],
                     [r, c - s], [r, c + s],
                     [r + s, c - s], [r + s, c], [r + s, c + s]]
        return filter(self.in_bounds, neighbors)

    def in_bounds(self, node):
        (r, c) = node
        return 0 <= r < self.grid.shape[0] and 0 <= c < self.grid.shape[1]

    def get_gscore(self, node):
        try:
            return self.gscore[tuple(node)]
        except KeyError:
            return float('inf')

    def compute_cost(self, current, neighbor):
        v = self.V(neighbor)
        n = self.N(current, neighbor)
        m = self.M(neighbor)
        d = self.D(neighbor)
        d2 = self.D2(neighbor)
        return 3*v+1*n+50*m+150*d+50*d2
        # return 2.5*v+1*n+50*m+130*d+0*d2

    def V(self, node):
        return abs(node[0] - self.start[0])

    def N(self, current, neighbor):
        if (current[0] == neighbor[0] or current[1] == neighbor[1]):
            return 10.0
        else:
            return 14.0

    def M(self, node):
        if self.grid[node[0], node[1]] == 1:
            return 0.0
        elif self.grid[node[0], node[1]] == 0:
            return 1.0

    def D(self, neighbor):
        return 1 / (1 + min(self.upward_obstacle(neighbor),
                            self.downward_obstacle(neighbor)))

    def D2(self, neighbor):
        return 1 / (1 + min(self.upward_obstacle(neighbor),
                            self.downward_obstacle(neighbor)) ** 2)

    def upward_obstacle(self, node):
        step = 1
        while(step <= 50):
            if self.grid[node[0] - step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def downward_obstacle(self, node):
        step = 1
        while(step <= 50):
            if self.grid[node[0] + step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def reconstruct_path(self, current):
        total_path = [current]
        while str(current) in self.parents:
            current = self.parents[str(current)]
            total_path.append(current)

        return total_path, self.close

    def print_info(self, current):
        # print 'gscore: ' + str(self.gscore)
        print 'current: ' + str(current)
        # print 'open: ' + str(self.open)
        # print 'close: ' + str(self.close)
        # print '------------------------------------'

    ###################
    # ----- JPS ----- #
    ###################

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

            new_gscore = self.gscore[tuple(node)] + \
                self.compute_cost(node, neighbor)

            if (str(jump_node) not in self.parents or
                    new_gscore < self.get_gscore(tuple(jump_node))):
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
