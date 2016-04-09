class Node():

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.gscore = float('inf')
        self.parent = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return '(' + str(self.row) + ', ' + str(self.col) + ')'

    def __hash__(self):
        return hash(str(self))

a = Node(4, 5)
b = Node(4, 4)
b.gscore = 1
a.gscore = 1
print a == b
print 'asd ' + str(a)
d = {}
d[a] = b
print a in d
r, c = a.row, a.col
print r, c
