"""
ESU Class

This class implements the ESU algorithm.
The class can identify subgraphs of specified size and return them for further\
    analysis or visualization.

Translated for networkx from https://github.com/IlyaVasUW/NEMO_SUITE/
"""

from typing import List
import networkx as nx
from networkx import Graph


class ESU:
    def __init__(self, G: nx.Graph, size: int):
        """
        Enumerates all unique subgraphs of a given motif size from the input\
                graph using the ESU algorithm.
        """
        self.G = G
        self.subgraph_list: List[Graph] = []
        self.size = size
        nodes = self.G.nodes()
        node_visited = set()

        for node in nodes:
            neighbor_set = set(self.get_right_neighbors(node))
            node_list = [node]
            node_visited.add(node)
            self.esu_recursive_helper(
                size, neighbor_set, node_list, self.subgraph_list, node_visited
            )

    def esu_recursive_helper(
        self,
        size: int,
        neighbors: set,
        node_list: list,
        subgraph_list: list,
        nodes_visited: set,
    ):
        if size == 1:
            subgraph_list.append(self.G.subgraph(node_list.copy()))
            return

        if len(neighbors) == 0:
            return

        for node in neighbors:
            node_list.append(node)
            nodes_visited.add(node)
            next_neighbors = set()

            for neighbor in neighbors:
                if neighbor not in nodes_visited:
                    next_neighbors.add(neighbor)
            for neighbor in self.G.neighbors(node):
                if neighbor not in nodes_visited:
                    next_neighbors.add(neighbor)

            self.esu_recursive_helper(
                size - 1,
                next_neighbors,
                node_list,
                subgraph_list,
                nodes_visited,
            )

            if len(node_list) > 0:
                node_list.pop()

        for node in neighbors:
            nodes_visited.discard(node)

    def get_right_neighbors(self, node):
        right_hand_neighbors = []
        nodes_list = list(self.G.nodes)
        node_index_in_g = nodes_list.index(node)

        for i, n in enumerate(self.G):
            if i > node_index_in_g and self.G.has_edge(node, n):
                right_hand_neighbors.append(n)

        return iter(right_hand_neighbors)

    def get_subgraph_list(self):
        return self.subgraph_list

    def number_of_subgraphs(self):
        return len(self.subgraph.list)
