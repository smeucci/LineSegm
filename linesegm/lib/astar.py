import numpy as np


class Astar():

    def __init__(self):
        pass

    def pathfind(self, im, start, goal):
        # size of the image
        self.size = im.shape
        # create openSet and closedSet
        self.closedSet = []
        self.openSet = []
        # initialize openSet, gScore, fScore with start node values
        self.openSet.append(start)
        self.gScore = {str(start): 0}
        self.fScore = {str(start): self.get_euclidean_dist(start, goal)}
        # create empty dictionary
        self.cameFrom = {}

        print '\t# start: ' + str(start) + " - goal: " + str(goal)

        while self.openSet:
            current = self.get_best_fScore()
            # print 'current: ' + str(current)
            # print 'open: ' + str(self.openSet)
            # print 'close: ' + str(self.closedSet)
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

                # cameFrom
                self.gScore[str(neighbor)] = tentative_gScore
                self.fScore[str(neighbor)] = self.gScore[str(neighbor)] + \
                    self.get_euclidean_dist(neighbor, goal)
                self.cameFrom[str(neighbor)] = current

    def get_euclidean_dist(self, current, goal):
        return np.sqrt((current[0] - goal[0])**2 + (current[1] + goal[1])**2)

    def get_neighbors(self, current):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0):
                    r = current[0] + i
                    c = current[1] + j
                    if (r >= 0 and c >= 0 and r <= self.size[0] and
                            c <= self.size[1]):
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
        return self.get_euclidean_dist(current, neighbor)

    def get_best_fScore(self):
        min = float('inf')
        for node in self.openSet:
            score = self.get_fScore(node)
            if score < min:
                min = score
                best = node

        return best

    def reconstruct_path(self, current):
        total_path = [current]
        while str(current) in self.cameFrom:
            current = self.cameFrom[str(current)]
            total_path.append(current)

        return total_path
