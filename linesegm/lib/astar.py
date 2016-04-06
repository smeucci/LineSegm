import numpy as np
import heapq


class PriorityQueue():

    def __init__(self):
        self.list = [0]
        self.list.pop()

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
        self.parent = {}
        self.open = PriorityQueue()
        self.close = []

    def pathfind(self, im, start, goal):
        # initialize
        self.im = im / 255
        self.start = start
        self.goal = goal
        self.open.put(self.start, self.heuristic(self.start, self.goal))
        self.gscore = np.zeros((self.im.shape), dtype=np.int32)
        self.gscore[tuple(self.start)] = 0

        print '\t# start: ' + str(self.start) + " - goal: " + str(self.goal)

        while not self.open.empty():

            if self.open.size() >= 10000:
                self.open.flush()

            current = self.open.get()
            self.print_info(current)

            if current == self.goal:
                return self.reconstruct_path(current)

            self.close.append(current)

            for neighbor in self.get_neighbors(current):

                if neighbor in self.close:
                    continue

                new_gscore = self.gscore[tuple(current)] + \
                    self.compute_cost(current, neighbor)

                if (str(neighbor) not in self.parent or
                        new_gscore < self.get_gscore(tuple(neighbor))):
                    self.gscore[tuple(neighbor)] = new_gscore
                    fscore = new_gscore + self.heuristic(neighbor, goal)
                    self.open.put(neighbor, fscore)
                    self.parent[str(neighbor)] = current

        return None

    def heuristic(self, current, goal):
        return 30*((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    def get_neighbors(self, current):
        r, c = current
        neighbors = [[r - 1, c - 1], [r - 1, c], [r - 1, c + 1],
                     [r, c - 1], [r, c + 1],
                     [r + 1, c - 1], [r + 1, c], [r + 1, c + 1]]
        return filter(self.in_bounds, neighbors)

    def in_bounds(self, node):
        (r, c) = node
        return 0 <= r < self.im.shape[0] and 0 <= c < self.im.shape[1]

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
        # return 3*v+1*n+50*m+150*d+50*d2
        return 2.5*v+1*n+50*m+130*d+0*d2

    def V(self, node):
        return abs(node[0] - self.start[0])

    def N(self, current, neighbor):
        if (current[0] == neighbor[0] or current[1] == neighbor[1]):
            return 10.0
        else:
            return 14.0

    def M(self, node):
        if self.im[node[0], node[1]] == 1:
            return 0.0
        elif self.im[node[0], node[1]] == 0:
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
            if self.im[node[0] - step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def downward_obstacle(self, node):
        step = 1
        while(step <= 50):
            if self.im[node[0] + step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def reconstruct_path(self, current):
        total_path = [current]
        while str(current) in self.parent:
            current = self.parent[str(current)]
            total_path.append(current)

        return total_path, self.close

    def print_info(self, current):
        # print 'gscore: ' + str(self.gscore)
        print 'current: ' + str(current)
        # print 'open: ' + str(self.open)
        # print 'close: ' + str(self.close)
        # print '------------------------------------'
