class Digraph:
    def __init__(self, V: int):
        self.V: int = V
        self.E: int = 0
        self.indegreeArr: list[int] = [0 for i in range(V)]
        self.adjacent = [[] for i in range(V)]

    def vertices(self):
        return self.V

    def edges(self):
        return self.E

    def validateVertex(self, v):
        if (v < 0 or v >= self.V):
            raise ValueError

    def addEdge(self, u, v, w):
        self.validateVertex(u)
        self.validateVertex(v)

        edge = self.Edge(u, v, w)
        self.adjacent[u].append(edge)
        self.indegreeArr[u] += 1
        self.E += 1

    def adj(self, v):
        self.validateVertex(v)
        return self.adjacent[v]

    def outdegree(self, v):
        self.validateVertex(v)
        return len(self.adjacent[v])

    def indegree(self, v):
        self.validateVertex(v)
        return self.indegreeArr[v]

    # def reverse(self):
    #     cls = self.__class__
    #     result = cls.__new__(cls)

    #     result.V = self.V
    #     result.E = self.E
    #     result.indegreeArr = [self.outdegree(v) for v in range(self.V)]
    #     for v in range(self.V):
    #         for e in self.adjacent[v]:


    class Edge:
        def __init__(self, u, v, w):
            self.u = u
            self.v = v
            self.w = w

        def __str__(self):
            return self.u.__str__() + " -(" + self.w.__str__() + ")-> " + self.v.__str__()

        def increaseWeight(self, w):
            self.w += w

        def reverse(self):
            cls = self.__class__
            result = cls.__new__(cls)

            result.u = self.v
            result.v = self.u
            result.w = self.w

            return result
