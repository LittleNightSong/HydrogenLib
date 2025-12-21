from typing import Any

from .stack import Stack
from .vis_structure import Visited


class GraphBase:
    def __init__(self, graph=None):
        """ initializes a directed graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        self.graph = graph or {}  # type: dict[Any, set[Any]]

    @classmethod
    def from_dict(cls, dct):
        g = cls()
        for k, v in dct.items():
            g.add_edge(k, v)
        return g

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.graph.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def children(self, vertex):
        return self.graph.get(vertex, set())

    def add_vertex(self, *vertexs):
        """ If the vertex "vertex" is not in
            self.graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
        """
        for vertex in vertexs:
            if vertex not in self.graph:
                self.graph[vertex] = set()

    def add_edge(self, left, right):
        """ assumes that edge is of type tuple (vertex1, vertex2);
            adds a directed edge from vertex1 to vertex2.
        """
        self.add_vertex(left, right)
        self.graph[left].add(right)

    def remove_edge(self, left, right):
        """ assumes that edge is of type tuple with two vertices """
        if self.exists(left) and right in self.children(left):
            self.graph[left].remove(right)

    def exists(self, vertex):
        return vertex in self.graph

    def __generate_edges(self):
        """ A static method generating the edges of the
            directed graph "graph". Edges are represented as lists
            with two vertices
        """
        edges = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                if [vertex, neighbour] not in edges:
                    edges.append([vertex, neighbour])
        return edges

    @property
    def circles(self):
        sck = Stack()
        vis = Visited()
        circle_vis = Visited()

        result = set()

        def func(current):
            sck.push(current)
            vis[current] = True

            for child in self.children(current):
                # print(f"Node {current} -> {child}")
                # print(sck)
                if vis[child]:  # 环的出现
                    # print(f'Find circle {child}')
                    ls = []
                    finded = False
                    for node in sck:
                        # print(f'Foreach Circle Node: {node}, finded={finded}')
                        if finded or node == child:
                            finded = True
                            circle_vis[node] = True
                            ls.append(node)
                    # ls.append(child)
                    # ls = ls[::-1]
                    result.add(tuple(ls))
                else:
                    func(child)

            vis[current] = False
            sck.pop()

        for vertex in self.vertices():
            if circle_vis[vertex]:
                continue  # 跳过已经遍历过的节点
            func(vertex)

        # func(1)

        return result

    def topological_sorted(self):
        visited = Visited()
        stack = Stack()

        def dfs(vertex):
            visited[vertex] = True
            for neighbour in self.graph.get(vertex, []):
                if not visited[neighbour]:
                    dfs(neighbour)
            stack.push(vertex)

        for vertex in self.vertices():
            if not visited[vertex]:
                dfs(vertex)

        return stack[::-1]

    def __str__(self):
        res = "vertices: "
        for k in self.graph:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


class UndirectedGraph(GraphBase):
    def __init__(self, graph=None):
        super().__init__(graph)

        for k in list(self.graph):
            for i in self.children(k):
                self.add_edge(k, i)

    def add_edge(self, left, right):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        super().add_edge(left, right)
        super().add_edge(right, left)

    def remove_edge(self, left, right):
        super().remove_edge(left, right)
        super().remove_edge(right, left)

    @property
    def circles(self):
        raise NotImplementedError("UndirectedGraph can't scan circles")


class WeightedGraph(GraphBase):
    class GraphItem:
        def __init__(self, value, weight):
            self.value, self.weight = value, weight

        def __hash__(self):
            return hash(self.value)

    @property
    def circles(self):
        raise NotImplementedError("WeightedGraph can't scan circles")

    def __init__(self, graph=None):
        super().__init__(graph)
        self.graph: dict[Any, dict[Any, Any]] = {}

    def add_vertex(self, *vertexs):
        for vertex in vertexs:
            if vertex not in self.graph:
                self.graph[vertex] = {}

    def add_edge(self, vertex1, vertex2):
        """ Adds a weighted edge between vertex1 and vertex2 """
        self.add_vertex(vertex1, vertex2)
        self.add_weighted_edge(vertex1, vertex2, None)

    def add_weighted_edge(self, vertex1, vertex2, weight):
        """ Adds a weighted edge between vertex1 and vertex2 """
        self.add_vertex(vertex1, vertex2)
        self.graph[vertex1][vertex2] = self.GraphItem(vertex2, weight)

    def get_weight(self, vertex1, vertex2):
        """ Returns the weight of the edge between vertex1 and vertex2 """
        if vertex2 in self.graph[vertex1]:
            return self.graph[vertex1][vertex2]
        return None

    def __str__(self):
        res = "vertices: "
        for k in self.graph:
            res += str(k) + " "
        res += "\nedges: "
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                res += f"{vertex} -> {neighbour}, weight={self.graph[vertex][neighbour]} "
        return res
