import networkx as nx
from typing import List
from networkx import Graph


def g6_label(graph: nx.Graph) -> str:
    """
    Return the g6label for Undirected graph.
    """
    # motifSize = n
    graph_size = graph.order()

    # first figure out the N(n)
    N = chr(graph_size + 63)

    # find x
    x = []
    diagonal_count: int
    column_count = graph_size
    for c in graph:
        diagonal_count = 0
        for r in graph:
            if diagonal_count < graph_size - column_count:
                x.append(graph.has_edge(r, c))
            else:
                break
            diagonal_count = diagonal_count + 1
        column_count = column_count - 1

    # attach 0's until x length is multiple of 6
    while len(x) % 6 != 0:
        x.append(0)

    # Compute R(x)
    # convert x into its ascii character to get R(x)
    R = ""
    r_char_list = [1] * int(len(x) / 6)
    i = 0
    while i < len(x):
        r_char_list[int(i / 6)] = (r_char_list[int(i / 6)] << 1) | x[i]
        if i % 6 == 5:
            r_char_list[int(i / 6)] = r_char_list[int(i / 6)] - 1
        i = i + 1
    for element in r_char_list:
        R = R + chr(element)
    return N + R


def d6_label(graph: nx.DiGraph) -> str:
    """
    Return the d6label for Directed graph.
    """
    # motifSize = n
    graph_size = graph.order()

    # first figure out the N(n)
    N = chr(graph_size + 63)

    # find x
    x = []
    for r in graph:
        for c in graph:
            x.append(graph.has_edge(r, c))

    # attach 0's until x length is multiple of 6
    while len(x) % 6 != 0:
        x.append(0)

    # convert x into its ascii character to get R(x)
    R = ""
    r_char_list = [1] * int(len(x) / 6)
    i = 0
    while i < len(x):
        r_char_list[int(i / 6)] = (r_char_list[int(i / 6)] << 1) | x[i]
        if i % 6 == 5:
            r_char_list[int(i / 6)] = r_char_list[int(i / 6)] - 1
        i = i + 1
    for element in r_char_list:
        R = R + chr(element)
    return N + R


def label_graph(networkx_graph, graph_type):  # networkx di or undi graph
    if graph_type == "Undirected":
        return g6_label(networkx_graph)
    if graph_type == "Directed":
        return d6_label(networkx_graph)


def export_labels(esu_list: List[Graph]):
    """
    Takes in esu subgraph list and output the labels into a .txt file.
    """
    return
