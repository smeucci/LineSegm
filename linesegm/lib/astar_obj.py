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


class Node():

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.gscore = float('inf')
        self.parent = None

    def __eq__(self, other):
        return (self.row == other.row and
                self.col == other.col)

    def __str__(self):
        return '(' + str(self.row) + ', ' + str(self.col) + ')'


class Astar():

    def __init__(self, grid):
        self.grid = grid / 255
        self.open = PriorityQueue()
        self.close = []
        self.step = 2

    def pathfind(self, start, goal):
        # initialize
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        self.start.gscore = 0
        self.open.put(self.start, self.heuristic(self.start, self.goal))

        while not self.open.empty():

            current = self.open.get()
            self.close.append(current)
            # print current

            if current == self.goal:
                return self.reconstruct_path(current)

            for neighbor in self.get_neighbors(current):

                if neighbor in self.close:
                    continue

                new_gscore = current.gscore + self.compute_cost(current, neighbor, self.start)

                if neighbor.parent is None or new_gscore < neighbor.gscore:
                    neighbor.gscore = new_gscore
                    fscore = new_gscore + self.heuristic(neighbor, self.goal)
                    neighbor.parent = current
                    self.open.put(neighbor, fscore)

        return None

    def heuristic(self, current, goal):
        return 40*((current.row - goal.row)**2 + (current.col - goal.col)**2)**0.5

    def get_neighbors(self, node):
        r, c = node.row, node.col
        s = self.step
        neighbors = [Node(r - s, c - s), Node(r - s, c), Node(r - s, c + s),
                     Node(r, c - s), Node(r, c + s),
                     Node(r + s, c - s), Node(r + s, c), Node(r + s, c + s)]
        return filter(self.in_bounds, neighbors)

    def in_bounds(self, node):
        r, c = node.row, node.col
        return 0 <= r < self.grid.shape[0] and 0 <= c < self.grid.shape[1]

    def compute_cost(self, current, neighbor, start):
        v = self.V(neighbor, start)
        n = self.N(current, neighbor)
        m = self.M(neighbor)
        d = self.D(neighbor)
        d2 = self.D2(neighbor)
        return 3*v+1*n+50*m+150*d+50*d2
        # return 2.5*v+1*n+50*m+130*d+0*d2

    def V(self, node, start):
        return abs(node.row - start.row)

    def N(self, current, neighbor):
        if (current.row == neighbor.row or current.col == neighbor.col):
            return 10.0
        else:
            return 14.0

    def M(self, node):
        r, c = node.row, node.col
        if self.grid[r, c] == 1:
            return 0.0
        elif self.grid[r, c] == 0:
            return 1.0

    def D(self, neighbor):
        return 1 / (1 + min(self.upward_obstacle(neighbor), self.downward_obstacle(neighbor)))

    def D2(self, neighbor):
        return 1 / (1 + min(self.upward_obstacle(neighbor), self.downward_obstacle(neighbor)) ** 2)

    def upward_obstacle(self, node):
        step = 1
        while(step <= 50):
            if self.grid[node.row - step, node.col] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def downward_obstacle(self, node):
        step = 1
        while(step <= 50):
            if self.grid[node.row + step, node.col] == 0:
                return float(step)
            else:
                step += 1

        return float('inf')

    def reconstruct_path(self, current):
        total_path = [[current.row, current.col]]
        while current.parent is not None:
            current = current.parent
            total_path.append([current.row, current.col])

        return total_path, self.close
