class Graph:
    node = []

    def find_node(self, node):
        return self.node[[x.state for x in self.node].index(node)]

    def bfs(self, node_name=None, directed=False):
        print()
        start = self.find_node(node_name) if node_name is not None else self.node[0]
        if len(self.node) == 0:
            return []
        queue = [start]
        solution = []
        edges = []
        while len(queue) != 0:
            temp = queue.pop(0)
            if not temp.marked:
                solution.append(temp)
            [queue.append(x.dest) for x in temp.trans if not x.dest.marked]
            edges.append([x.alpha for x in temp.trans if not x.dest.marked])
            temp.marked = True
            if not directed:
                [queue.append(x) for x in temp.back if not x.marked]
        for x in self.node:
            x.marked = False
        print(edges)
        print(solution)
        return solution


class Node:
    state = ""
    trans = []
    marked = False
    back = []

    def __init__(self, st="", tr=None, back=None):
        tr = [] if tr is None else tr
        back = [] if back is None else back
        self.trans = tr
        self.back = back
        self.state = st


class Transition:
    dest = Node()
    alpha = ""

    def __init__(self, dest, a):
        self.dest = dest
        self.alpha = a
