#!/usr/bin/env python3
import argparse
import sys
from collections import deque


class Graph:
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


def parse_graph(input_data):
    g = Graph()
    for line in input_data.strip().split("\n"):
        if ":" not in line:
            continue
        node_str, neighbors_str = line.split(":", 1)
        node = node_str.strip()
        g.add_node(node)
        
        neighbors_str = neighbors_str.strip()
        if not neighbors_str:
            continue
            
        for neighbor_str in neighbors_str.split(","):
            neighbor_str = neighbor_str.strip()
            if not neighbor_str:
                continue
            if "(w=" in neighbor_str:
                neighbor_part, weight_part = neighbor_str.split("(w=", 1)
                neighbor = neighbor_part.strip()
                weight = int(weight_part.rstrip(")"))
                g.add_edge(node, neighbor, weight)
            else:
                g.add_edge(node, neighbor_str.strip(), None)
    
    return g


def bfs(g, start=None):
    if start is None:
        start = sorted(g.get_nodes())[0]
    
    visited = set()
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        
        neighbors = sorted(g.get_neighbors(node))
        for neighbor, weight in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
    
    return order


def main():
    parser = argparse.ArgumentParser(description="BFS traversal of a graph")
    parser.add_argument("-f", "--file", type=str, help="Input file containing graph in list format")
    parser.add_argument("-s", "--start", type=str, help="Starting node for BFS")
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r") as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()
    
    g = parse_graph(input_data)
    start_node = args.start if args.start else sorted(g.get_nodes())[0]
    result = bfs(g, start_node)
    
    print(" -> ".join(result))


if __name__ == "__main__":
    main()
