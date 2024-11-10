import networkx as nx
from src.types import GraphType


def graph6(graph: nx.Graph) -> str:
    """
    Convert a subgraph into graph6 format.
    """
    # Step 1: Compute N(n), the graph size character
    graph_size = graph.order()
    N = chr(graph_size + 63)

    # Step 2: Compute R(x). Create bit vector from the upper triangle of the
    # adjacency matrix
    # For undirected: read upper triangle of the matrix, column by column
    bit_vector = []
    for c in range(graph_size):
        for r in range(c):
            bit_vector.append(1 if graph.has_edge(r, c) else 0)

    # Step 3: Pad bit vector with zeros to make its length a multiple of 6
    while len(bit_vector) % 6 != 0:
        bit_vector.append(0)

    # Step 4: Convert each group of 6 bits into an ASCII character for encoding
    R = ""
    for i in range(0, len(bit_vector), 6):
        group = bit_vector[i:i + 6]
        group_value = sum((bit << (5 - idx)) for idx, bit in enumerate(group))
        R += chr(group_value + 63)
    return N + R


def digraph6(graph: nx.DiGraph) -> str:
    """
    Convert a directed subgraph into digraph6 format.
    """
    # Step 1: Compute N(n), the graph size character
    graph_size = graph.order()
    N = chr(graph_size + 63)

    # Step 2: Compute R(x). Create bit vector from the upper triangle of the
    # adjacency matrix
    # For directed: read the matrix row by row
    bit_vector = []
    for r in range(graph_size):
        for c in range(graph_size):
            bit_vector.append(1 if graph.has_edge(r, c) else 0)

    # Step 3: Pad bit vector with zeros to make its length a multiple of 6
    while len(bit_vector) % 6 != 0:
        bit_vector.append(0)

    # Step 4: Convert each group of 6 bits to an ASCII character for encoding
    R = ""
    for i in range(0, len(bit_vector), 6):
        group = bit_vector[i:i + 6]
        group_value = sum((bit << (5 - idx)) for idx, bit in enumerate(group))
        R += chr(group_value + 63)

    return N + R


def get_graph_label(nx_graph: nx.Graph, graph_type: GraphType) -> str:
    """
    Label a graph in either graph6 (undirected) or digraph6 (directed) format.
    """
    if graph_type == GraphType.UNDIRECTED:
        return graph6(nx_graph)
    if graph_type == GraphType.DIRECTED:
        return digraph6(nx_graph)
