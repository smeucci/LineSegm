import numpy as np


class Astar():

    def __init__(self):
        pass

    def pathfind(self, im, start, goal):
        # initialize image, start and goal
        self.im = im / 255
        self.size = self.im.shape
        self.map = np.zeros((self.size[0], self.size[1]), dtype=np.int32)
        self.start = start
        self.goal = goal
        # create openSet and closedSet
        self.closedSet = []
        self.openSet = [start]
        self.cameFrom = {}
        # initialize openSet, gScore, fScore with start node values
        self.gScore = {str(start): 0}
        self.fScore = {str(start): self.get_euclidean_dist(start, goal)}
        self.map[start[0], start[1]] = self.fScore[str(start)]

        print '\t# start: ' + str(start) + " - goal: " + str(goal)
        cnt = 0
        while self.openSet:
            current = self.get_best_fScore()
            # print 'fscore: ' + str(self.fScore)
            # print 'gscore: ' + str(self.gScore)
            print 'current: ' + str(current)
            # print 'open: ' + str(self.openSet)
            # print 'close: ' + str(self.closedSet)
            # print '------------------------------------'
            cnt += 1
            # print cnt
            if current == goal:
                return self.reconstruct_path(current)

            self.openSet.remove(current)
            self.closedSet.append(current)
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor in self.closedSet:
                    continue
                tentative_gScore = self.get_tentative_gScore(current, neighbor)

                if neighbor not in self.openSet:
                    self.openSet.append(neighbor)
                elif tentative_gScore >= self.get_gScore(neighbor):
                    continue

                self.gScore[str(neighbor)] = tentative_gScore
                self.fScore[str(neighbor)] = self.gScore[str(neighbor)] + \
                    self.get_euclidean_dist(neighbor, goal)
                self.cameFrom[str(neighbor)] = current
                self.map[neighbor[0], neighbor[1]] = self.fScore[str(neighbor)]

        return None

    def get_euclidean_dist(self, current, goal):
        return 20*((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    def get_neighbors(self, current):
        r, c = current
        neighbors = [[r - 1, c - 1], [r - 1, c], [r - 1, c + 1],
                     [r, c - 1], [r, c + 1],
                     [r + 1, c - 1], [r + 1, c], [r + 1, c + 1]]
        return filter(self.in_bounds, neighbors)

    def in_bounds(self, node):
        (r, c) = node
        return 0 <= r < self.size[0] and 0 <= c < self.size[1]

    def get_gScore(self, node):
        try:
            return self.gScore[str(node)]
        except KeyError:
            return float('inf')

    def get_fScore(self, node):
        try:
            return self.fScore[str(node)]
        except KeyError:
            return float('inf')

    def get_tentative_gScore(self, current, neighbor):
        return self.gScore[str(current)] + \
            self.get_heuristic_cost(current, neighbor)

    def get_heuristic_cost(self, current, neighbor):
        # not implemented yet, placeholder
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
        max_steps = 50
        while(step <= max_steps):
            if self.im[node[0] - step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def downward_obstacle(self, node):
        step = 1
        max_steps = 50
        while(step <= max_steps):
            if self.im[node[0] + step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def get_best_fScore(self):
        min = float('inf')
        for node in self.openSet:
            score = self.get_fScore(node)
            if score <= min:
                min = score
                best = node

        return best

    def reconstruct_path(self, current):
        total_path = [current]
        while str(current) in self.cameFrom:
            current = self.cameFrom[str(current)]
            total_path.append(current)

        return total_path, self.map  # , self.closedSet
