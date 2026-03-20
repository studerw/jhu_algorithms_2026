import random
import argparse
import string

class Graph:
    """A flexible adjacency list representation for graph algorithms."""
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v, weight=None):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, u):
        return self.adj.get(u, [])

    def get_nodes(self):
        return list(self.adj.keys())

    def print_graph(self, format="list"):
        """Prints the graph in either 'list' or 'matrix' format."""
        nodes = sorted(self.adj.keys())
        if format == "list":
            print(str(self))
        elif format == "matrix":
            # Header
            print("    " + " ".join(f"{n:3}" for n in nodes))
            for u in nodes:
                row = []
                for v in nodes:
                    # Find if there is an edge u -> v
                    weight = next((w for neighbor, w in self.adj[u] if neighbor == v), None)
                    if u == v:
                        row.append("0")
                    elif weight is not None:
                        row.append(str(weight))
                    elif any(neighbor == v for neighbor, w in self.adj[u]):
                        row.append("1")
                    else:
                        row.append("-")
                print(f"{u:3} " + " ".join(f"{val:3}" for val in row))

    def __str__(self):
        result = []
        # Sort nodes for consistent output
        for u in sorted(self.adj.keys()):
            neighbors = ", ".join([f"{v}(w={w})" if w is not None else str(v) for v, w in self.adj[u]])
            result.append(f"{u}: {neighbors}")
        return "\n".join(result)

def get_node_label(i):
    """Returns A, B, C... for i < 26, otherwise v26, v27..."""
    if i < 26:
        return string.ascii_uppercase[i]
    return f"v{i}"

def generate_random_graph(n, m, directed=False, weighted=False, max_weight=10):
    """
    Generates a random graph with n nodes (A, B, C...) and m edges.
    Uses the G(n, m) model where m edges are chosen uniformly at random.
    """
    g = Graph(directed=directed)
    nodes = [get_node_label(i) for i in range(n)]
    for node in nodes:
        g.add_node(node)
    
    # Generate all possible edges (excluding self-loops)
    possible_edges = []
    for i in range(n):
        for j in range(n):
            if i != j:
                u, v = nodes[i], nodes[j]
                if directed or i < j:
                    possible_edges.append((u, v))
    
    # Cap m if it's too high for the number of nodes
    if m > len(possible_edges):
        print(f"Warning: m={m} is too large for n={n} nodes. Capping at {len(possible_edges)}.")
        m = len(possible_edges)
        
    edges = random.sample(possible_edges, m)
    for u, v in edges:
        weight = random.randint(1, max_weight) if weighted else None
        g.add_edge(u, v, weight)
    
    return g

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random graph.")
    parser.add_argument("-n", "--nodes", type=int, default=5, help="Number of nodes")
    parser.add_argument("-m", "--edges", type=int, default=7, help="Number of edges")
    parser.add_argument("-w", "--weighted", action="store_true", help="Generate a weighted graph")
    parser.add_argument("-d", "--directed", action="store_true", help="Generate a directed graph")
    parser.add_argument("-f", "--format", choices=["list", "matrix"], default="list", help="Output format (list or matrix)")
    
    args = parser.parse_args()
    
    print(f"--- Generating Random Graph (n={args.nodes}, m={args.edges}, weighted={args.weighted}, directed={args.directed}) ---")
    random_graph = generate_random_graph(args.nodes, args.edges, directed=args.directed, weighted=args.weighted)
    random_graph.print_graph(format=args.format)
