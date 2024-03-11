import numpy as np
import networkx as nx


def read_array_of_edges(filename: str) -> tuple[tuple[int], int]:
    """Reads an array of edges from the given text file.

    Args:
        filename (str): name of the file containing number of vertices
        in the first line, number of edges in the second line, vertices
        that have edges as X Y for the rest of the file.

    Returns:
        tuple[tuple[int], int]: a tuple containing edges as a list of tuples and
        an integer for number of vertices -> (edge_list, num_vertices)
    """
    with open(filename, "r") as f:
        V = int(f.readline())
        if V < 0:
            raise ValueError("Number of vertices must be non negative")

        E = int(f.readline())
        if E < 0:
            raise ValueError("Number of vertices must be non negative")

        edges = []
        for _ in range(E):
            v, w = map(int, f.readline().split())
            edges.append((v, w))

    return edges, V


class Graph:
    """Undirected graph with adjacency list representation.
    Adapted from: https://algs4.cs.princeton.edu/41graph/Graph.java.html
    """

    def __init__(self, V: int) -> None:
        self.V = V
        self.E = 0
        self._adj = []
        for _ in range(self.V):
            self._adj.append([])

    def __str__(self) -> str:
        s = ""
        s += f"{self.V} vertices, {self.E} edges\n"
        for v in range(self.V):
            s += f"{v}: "
            for w in self.adj[v]:
                s += f"{w} "
            s += "\n"
        return s

    @property
    def adj(self):
        return self._adj

    @adj.getter
    def adj(self):
        return self._adj

    @adj.setter
    def adj(self, edge: tuple[int, int]):
        self._adj[edge[0]].append(edge[1])

    def validate_vertex(self, v: int) -> None:
        if v < 0 or v >= self.V:
            raise ValueError(f"Vertex {v} is not between 0 and {self.V-1}")

    def add_edge(self, v: int, w: int) -> None:
        """
        Adds the undirected edge v-w to this graph.
        Args:
            v (int): one vertex in the edge
            w (int): the other vertex in the edge
        Returns:
            None
        """
        self.validate_vertex(v)
        self.validate_vertex(w)

        self.E += 1
        if v != w:
            self.adj = (w, v)
        self.adj = (v, w)

    def degree(self, v: int) -> int:
        """
        Returns the degree (num. of connections) of vertex v.
        Checks the length of the adj. array length of given vertex.
        Args:
            v (int): the vertex
        Returns:
            int: the degree of vertex v
        """
        self.validate_vertex(v)
        return len(self.adj[v])

    def max_degree(self) -> int:
        """Find maximum degree of the graph.
        Calculates degree for each vertex and returns
        the maximum.

        Returns:
            int: maximuum degree
        """
        max = 0
        for v in range(self.V):
            degree = self.degree(v)
            if degree > max:
                max = degree
        return max

    def self_loops(self) -> int:
        """Returns the number of self loops in a graph.
        Search for entry v in the list of connections for each
        v in the graph.

        Returns:
            int: num. of self loops
        """
        count = 0
        for v in range(self.V):
            for w in self.adj[v]:
                if v == w:
                    count += 1
        return count

    def to_networkx(self) -> nx.Graph:
        """Convert graph to networkx format.

        Returns:
            nx.Graph: networkx graph
        """
        G = nx.Graph()
        for v in range(self.V):
            for w in self.adj[v]:
                if not G.has_edge(v, w):
                    G.add_edge(v, w)
        return G

    @classmethod
    def load(cls, filename: str):
        edges, V = read_array_of_edges(filename)
        g = cls(V)

        for edge in edges:
            g.add_edge(edge[0], edge[1])

        return g


class AdjMatrixGraph(Graph):
    """Undirected graph with adjacency list representation.
    Adapted from: https://algs4.cs.princeton.edu/41graph/Graph.java.html
    """

    def __init__(self, V: int) -> None:
        super().__init__(V)
        self._adj = np.zeros((V, V), dtype=bool)

    def __str__(self) -> str:
        s = ""
        s += f"{self.V} vertices, {self.E} edges\n"
        for v in range(self.V):
            s += f"{v}: "
            for w in np.where(self.adj[v])[0]:
                s += f"{w} "
            s += "\n"
        return s

    @property
    def adj(self):
        return self._adj

    @adj.getter
    def adj(self):
        return self._adj

    @adj.setter
    def adj(self, edge: tuple[int, int]):
        self._adj[edge[0]][edge[1]] = True

    def degree(self, v: int) -> int:
        """
        Returns the degree (num. of connections) of vertex v.
        Checks the length of the adj. array length of given vertex.
        Args:
            v (int): the vertex
        Returns:
            int: the degree of vertex v
        """
        self.validate_vertex(v)
        return self.adj[v].sum()

    def self_loops(self) -> int:
        """Returns the number of self loops in a graph.
        Search for entry v in the list of connections for each
        v in the graph.

        Returns:
            int: num. of self loops
        """
        count = 0
        for v in range(self.V):
            if self.adj[v][v]:
                count += 1
        return count

    def to_networkx(self) -> nx.Graph:
        """Convert graph to networkx format.

        Returns:
            nx.Graph: networkx graph
        """
        G = nx.Graph()
        for v in range(self.V):
            for w in np.where(self.adj[v])[0]:
                if not G.has_edge(v, w):
                    G.add_edge(v, w)
        return G

    @classmethod
    def load(cls, filename: str):
        edges, V = read_array_of_edges(filename)
        g = cls(V)

        for edge in edges:
            g.add_edge(edge[0], edge[1])

        return g
