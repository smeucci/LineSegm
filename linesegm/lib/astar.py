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

    def __init__(self, grid):
        self.parents = {}
        self.open = PriorityQueue()
        self.close = []
        self.grid = grid / 255
        self.gscore = np.zeros((self.grid.shape), dtype=np.int32)
        # print self.grid
        self.step = 2

    def pathfind(self, start, goal):
        # initialize
        self.start = start
        self.goal = goal
        self.gscore[tuple(self.start)] = 0
        self.open.put(self.start, self.heuristic(self.start, self.goal))
        print 'start: ' + str(self.start) + " - goal: " + str(self.goal),

        while not self.open.empty():

            current = self.open.get()
            self.print_info(current)

            if current == self.goal:
                return self.reconstruct_path(current)

            self.close.append(current)

            for neighbor in self.get_neighbors(current):

                if neighbor in self.close:
                    continue

                new_gscore = self.gscore[tuple(current)] + self.compute_cost(current, neighbor, self.start)

                if (str(neighbor) not in self.parents or new_gscore < self.get_gscore(tuple(neighbor))):
                    self.gscore[tuple(neighbor)] = new_gscore
                    self.parents[str(neighbor)] = current
                    fscore = new_gscore + self.heuristic(neighbor, self.goal)
                    self.open.put(neighbor, fscore)

        return None

    def heuristic(self, current, goal):
        # return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return 40*((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    def get_neighbors(self, node):
        r, c = node
        s = self.step
        neighbors = [[r - s, c - s], [r - s, c], [r - s, c + s],
                     [r, c - s], [r, c + s],
                     [r + s, c - s], [r + s, c], [r + s, c + s]]
        return filter(self.in_bounds, neighbors)
        # return filter(self.walkable, neighbors)

    def in_bounds(self, node):
        r, c = node
        return 0 <= r < self.grid.shape[0] and 0 <= c < self.grid.shape[1]

    def walkable(self, node):
        r, c = node
        try:
            if self.in_bounds(node) and self.grid[r, c] == 1:
                return True
            else:
                return False
        except IndexError:
            return False

    def get_gscore(self, node):
        try:
            return self.gscore[tuple(node)]
        except KeyError:
            return float('inf')

    def compute_cost(self, current, neighbor, start):
        v = self.V(neighbor, start)
        n = self.N(current, neighbor)
        m = self.M(neighbor)
        d = self.D(neighbor)
        d2 = self.D2(neighbor)
        return 3*v+1*n+50*m+150*d+50*d2
        # return 2.5*v+1*n+50*m+130*d+0*d2

    def V(self, node, start):
        return abs(node[0] - start[0])

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
        return 1 / (1 + min(self.upward_obstacle(neighbor), self.downward_obstacle(neighbor)))

    def D2(self, neighbor):
        return 1 / (1 + min(self.upward_obstacle(neighbor), self.downward_obstacle(neighbor)) ** 2)

    def upward_obstacle(self, node):
        step = 1
        try:
            while(step <= 50):
                if self.grid[node[0] - step, node[1]] == 0:
                    return float(step)
                else:
                    step += 1

            return float('inf')
        except IndexError:
            return float('inf')

    def downward_obstacle(self, node):
        step = 1
        try:
            while(step <= 50):
                if self.grid[node[0] + step, node[1]] == 0:
                    return float(step)
                else:
                    step += 1

            return float('inf')
        except IndexError:
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
