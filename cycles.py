class Edge:
    def __init__(self, u, v, flow, capacity, rev):
        self.u = u
        self.v = v
        self.flow = flow
        self.capacity = capacity
        self.rev = rev

class Graph:
    def __init__(self, n, sNodes, tNodes):
        self.adj = [[] for i in range(n)]
        self.n = n
        self.level = [0 for i in range(n)]
        self.sNodes = sNodes
        self.tNodes = tNodes

    # add edge to the graph
    def addEdge(self, u, v, C):
        forward = Edge(u, v, 0, C, len(self.adj[v]))
        backward = Edge(v, u, 0, 0, len(self.adj[u]))
        if forward not in self.adj[u]:
            # print ("adding edge", u, v, C)
            self.adj[u].append(forward)
        if backward not in self.adj[v]:
            self.adj[v].append(backward)

    # finds if more flow can be sent from s to t
    def BFS(self, s, t):
        for i in range(self.n):
            self.level[i] = -1

        # level of source vertex
        self.level[s] = 0
        queue = [s]
        while queue:
            u = queue.pop(0)
            for i in range(len(self.adj[u])):
                node = self.adj[u][i]
                if self.level[node.v] < 0 and node.flow < node.capacity:
                    # flowable
                    # level of current vertex is level of parent + 1
                    self.level[node.v] = self.level[u] + 1
                    queue.append(node.v)

        return self.level[t] >= 0

    def sendFlow(self, u, flow, t, store, edgeSet):
        if u == t: return flow
        # traverse all adjacent edges one -by -one
        while store[u] < len(self.adj[u]):
            # pick next edge from adjacency list of u
            node = self.adj[u][store[u]]
            if self.level[node.v] == self.level[u]+1 and node.flow < node.capacity:
                # find minimum flow from u to t
                curr = min(flow, node.capacity - node.flow)
                moreFlow = self.sendFlow(node.v, curr, t, store, edgeSet)
                
                # flow is greater than zero
                if moreFlow and moreFlow > 0:
                    # add flow to current edge
                    node.flow += moreFlow
                    # add new edges if it is a forward edge
                    if (node.u in self.sNodes and node.v in self.tNodes):
                        edgeSet.append((node.u, node.v))
                    # if we are undoing edge, undo in edgeSet
                    else:
                        if ((node.v, node.u)) in edgeSet:
                            edgeSet.remove((node.v, node.u))

                    # subtract flow from reverse edge of current edge
                    self.adj[node.v][node.rev].flow -= moreFlow
                    return moreFlow
            store[u] += 1

    # returns maximum flow in graph
    def dinic(self, s, t):
        if s == t: return -1
        # initialize result
        total = 0
        edgeSet = []
        while self.BFS(s, t) == True:
            store = [0 for i in range(self.n+1)]
            while True:
                flow = self.sendFlow(s, float('inf'), t, store, edgeSet)
                # no more augmenting path
                if not flow:
                    break
                # add path flow to overall flow
                total += flow

        return (total, edgeSet)

def bipartite(sNodes, tNodes, adj):
    rest = set(adj.keys())
    while len(rest) > 0:
        # print("rest = ", rest)
        first = list(rest)[0]
        queue = [first]
        sNodes.add(first)
        rest.remove(first)
        while queue:
            u = queue.pop(0)
            if u in sNodes:
                for v in adj[u]:
                    if v in rest:
                        if v in sNodes:
                            return False
                        rest.remove(v)
                        # print("rest = ", rest)
                        queue.append(v)
                        tNodes.add(v)
            else:
                for v in adj[u]:
                    if v in rest:
                        if v in tNodes:
                            return False
                        rest.remove(v)
                        # print("rest = ", rest)
                        queue.append(v)
                        sNodes.add(v)
        # print("rest after one parse = ", rest)

        
    # print(queue)
    # print(sNodes, tNodes)
    return len(sNodes) == len(tNodes)
        

def drawGraph(row, col, edgeSet, node, nodeToIndex):
    edgeSet = sorted(edgeSet, key = lambda k : (k[0], k[1]))
    # print(edgeSet)
    # print(nodeToIndex)
    adj = {}
    for i in range(node+1):
        adj[i] = set()
    for (x, y) in edgeSet:
        if x != 0 and y != node:
            adj[x].add(y)
            adj[y].add(x)
    
    result = [["x" for _ in range(col)] for _ in range(row)]
    
    keys = list(adj.keys())[1:-1]
    # print(keys)
    for key in keys:
        (r, c) = nodeToIndex[key]
        neighbors = list(map(lambda x : nodeToIndex[x], adj[key]))
        # print(neighbors)
        if neighbors[0][0] < neighbors[1][0]:
            (r1, c1) = neighbors[0]
            (r2, c2) = neighbors[1]
        else:
            (r1, c1) = neighbors[1]
            (r2, c2) = neighbors[0]

        #r1 <= r2

        # print((r, c), (r1, c1), (r2, c2))

        if r == r1 == r2:
            # print(r, c, "-")
            result[r][c] = "-"
        elif c == c1 == c2:
            # print(r, c, "|")
            result[r][c] = "|"
        elif (r == r1 and c1 == c + 1 and c == c2 and r2 == r + 1):
            # print(r, c, "r")
            result[r][c] = "r"
        elif (r == r1 and c1 == c - 1 and c == c2 and r2 == r + 1):
            # print(r, c, "7")
            result[r][c] = "7"
        elif (r == r2 and c2 == c + 1 and c == c1 and r1 == r - 1):
            # print(r, c, "L")
            result[r][c] = "L"
        elif (r == r2 and c2 == c - 1 and c == c1 and r1 == r - 1):
            # print(r, c, "J")
            result[r][c] = "J"
        else:
            print("???")
        
    for row in result:
        print("".join(row))



def main():
    # step 0. process read in
    row, col = tuple([int(x) for x in input().split()])
    matrix = []
    got = 0
    while (got < row):
        r = input()
        temp = []
        for i in range(0, col):
            temp.append(r[i])
        matrix.append(temp)
        got += 1

    # build edge graph 
    # mark node as 1, 2, ... n
    # the source is 0 and target is n+1
    # so there are n+2 nodes in total

    nodeToIndex = {}
    IndexToNode = {}
    node = 1
    edge = []
    adj = {}
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == ".":
                nodeToIndex[node] = (r, c)
                IndexToNode[(r, c)] = node
                adj[node] = []
                node += 1


    sNodes = set()
    tNodes = set()


    adjList = {}
    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == ".":
                adjList[IndexToNode[(r, c)]] = []


    for r in range(len(matrix)):
        for c in range(len(matrix[r])):
            if matrix[r][c] == "." and r+1 < len(matrix) and matrix[r+1][c] == ".":
                edge.append((IndexToNode[(r, c)], IndexToNode[(r+1, c)]))
                adj[IndexToNode[(r, c)]].append(IndexToNode[(r+1, c)])

                adjList[IndexToNode[(r, c)]].append(IndexToNode[(r+1, c)])

            if matrix[r][c] == "." and c+1 < len(matrix[r]) and matrix[r][c+1] == ".":
                edge.append((IndexToNode[(r, c)], IndexToNode[(r, c+1)]))
                adj[IndexToNode[(r, c)]].append(IndexToNode[(r, c+1)])

                adjList[IndexToNode[(r, c)]].append(IndexToNode[(r, c+1)])

            if matrix[r][c] == "." and r-1 >= 0 and matrix[r-1][c] == ".":
                adjList[IndexToNode[(r, c)]].append(IndexToNode[(r-1, c)])

            if matrix[r][c] == "." and c-1 >= 0 and matrix[r][c-1] == ".":
                adjList[IndexToNode[(r, c)]].append(IndexToNode[(r, c-1)])
            




    if not adj:
        # no any connected edges
        return False
    

    

    result = bipartite(sNodes, tNodes, adjList)
    # print(sNodes, tNodes)
    # print(adj)
    if not result:
        print("NO")
    else:
        g = Graph(node+1, sNodes, tNodes)
        for (u, v) in edge:
            if u in sNodes: g.addEdge(u, v, 1)
            elif v in sNodes: g.addEdge(v, u, 1)
        else: g.addEdge(v, u, 1)
        for u in sNodes:
            g.addEdge(0, u, 2)
        for v in tNodes:
            g.addEdge(v, node, 2)
        
        maxFlow, edgeSet = g.dinic(0, node)
        # print(maxFlow)
        # print(edgeSet)

        if maxFlow == node - 1: 
            print("YES")
            (drawGraph(row, col, edgeSet, node, nodeToIndex))
        else: 
            print("NO")




    



main()