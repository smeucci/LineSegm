

class Astar():

    def __init__(self):
        pass

    def pathfind(self, im, start, goal):
        # initialize image, start and goal
        self.im = im / 255
        self.start = start
        self.goal = goal
        # size of the image
        self.size = self.im.shape
        # create openSet and closedSet
        self.closedSet = []
        self.openSet = []
        # initialize openSet, gScore, fScore with start node values
        self.openSet.append(start)
        self.gScore = {str(start): 0}
        self.fScore = {str(start): 20*self.get_euclidean_dist(start, goal)}
        # create empty dictionary
        self.cameFrom = {}

        print '\t# start: ' + str(start) + " - goal: " + str(goal)
        cnt = 0
        while self.openSet:
            current = self.get_best_fScore()
            # print 'fscore: ' + str(self.fScore)
            # print 'gscore: ' + str(self.gScore)
            # print 'current: ' + str(current)
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
                    20*self.get_euclidean_dist(neighbor, goal)
                self.cameFrom[str(neighbor)] = current

        return None

    def get_euclidean_dist(self, current, goal):
        return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2) ** 0.5

    def get_neighbors(self, current):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0):
                    r = current[0] + i
                    c = current[1] + j
                    if (r >= 0 and c >= 0 and r <= self.size[0]-1 and
                            c <= self.size[1]-1):
                        neighbor = [r, c]
                        neighbors.append(neighbor)

        return neighbors

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
        max_steps = 50
        while(step <= max_steps):
            if self.im[node[0] - step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float(max_steps)

    def downward_obstacle(self, node):
        step = 1
        max_steps = 50
        while(step <= max_steps):
            if self.im[node[0] + step, node[1]] == 0:
                return float(step)
            else:
                step += 1

        return float(max_steps)

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

        return total_path  # , self.closedSet
