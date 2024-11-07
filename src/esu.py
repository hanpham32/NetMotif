"""
ESU Class

This class implements the ESU algorithm.
The class can identify subgraphs of specified size and return them for further\
    analysis or visualization.

"""

import networkx as nx
import random


class ESU:
    def __init__(self, G: nx.Graph):
        self.G = G

    #currently does not allow for motif size over 10 because of default sample probability. should be fixed
    def enumerate_subgraphs(self, size: int, sample_probability: list[float] = [1,1,1,1,1,1,1,1,1,1]):
        """
        Enumerates all unique subgraphs of a given motif size from the input\
                graph using the ESU algorithm.
        Translated and improved for networkx from https://github.com/IlyaVasUW/NEMO_SUITE/
        """
        subgraph_list = []
        nodes = self.G.nodes()
        node_visited = set()

        sample_neighbors = self.eliminate_percentage(nodes, sample_probability[0])

        for node in sample_neighbors:
            neighbor_set = set(self.get_right_neighbors(node))
            node_list = [node]
            node_visited.add(node)
            self.esu_recursive_helper(size, neighbor_set, node_list, subgraph_list, node_visited)

        return subgraph_list

    def esu_recursive_helper(self, size: int, neighbors: set, node_list: list, subgraph_list: list, nodes_visited: set,  sample_probability: list[float]):
        if size == 1:
            subgraph_list.append(self.G.subgraph(node_list.copy()))
            return

        if len(neighbors) == 0:
            return

        sample_neighbors = self.eliminate_percentage(neighbors, sample_probability[len(node_list)])

        for node in sample_neighbors:
            node_list.append(node)
            nodes_visited.add(node)
            next_neighbors = set()

            for neighbor in sample_neighbors:
                if neighbor not in nodes_visited:
                    next_neighbors.add(neighbor)
            for neighbor in self.G.neighbors(node):
                if neighbor not in nodes_visited:
                    next_neighbors.add(neighbor)

            self.esu_recursive_helper(size - 1, next_neighbors, node_list, subgraph_list, nodes_visited)

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

    #Removes a given percentage of elements from a list randomly.
    def eliminate_percentage(set: set, probability: float):
        num_to_remove = int(len(set) * probability)
        indices_to_remove = random.sample(range(len(set)), num_to_remove)

        # Remove elements in reverse order to avoid index issues
        for i in sorted(indices_to_remove, reverse=True):
            set.pop(i)

        return set

