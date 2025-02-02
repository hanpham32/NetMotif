import networkx as nx
from src.types import GraphType
import os
import subprocess
import streamlit as st

def graph6(graph: nx.Graph) -> str:
    """
    Convert a subgraph into graph6 format.

    Parameters:
        graph (nx.Graph): A NetworkX graph.

    Returns:
        str: The graph6 encoded string.
    """
    # Step 1: Compute N(n), the graph size character
    graph_size = graph.order()  # number of nodes in the graph
    vertices = list(graph.nodes())
    n = len(vertices)

    if graph_size == 0:
        return ""  # empty graph
    elif graph_size == 1:
        return ""  # single-node graph

    N = chr(graph_size + 63)  # add 63 to graph_size

    # Step 2: Compute R(x). Create bit vector from the upper triangle of the
    # adjacency matrix
    # For undirected: read upper triangle of the matrix, column by column
    bit_vector = []
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for r in range(len(adj_matrix)):
        for c in range(len(adj_matrix[r])):
            if graph.has_edge(vertices[r], vertices[c]):
                adj_matrix[r][c] = 1
    for col in range(len(adj_matrix[0])):
        for row in range(col):
            bit_vector.append(adj_matrix[row][col])

    # Step 3: Pad bit vector with zeros to make its length a multiple of 6
    while len(bit_vector) % 6 != 0:
        bit_vector.append(0)

    # Step 4: Convert each group of 6 bits into an ASCII character for encoding
    R = ""
    for i in range(0, len(bit_vector), 6):
        group = bit_vector[i : i + 6]
        group_value = sum((bit << (5 - idx)) for idx, bit in enumerate(group))
        R += chr(group_value + 63)
    return N + R


def digraph6(graph: nx.DiGraph) -> str:
    """
    Convert a directed subgraph into digraph6 format.

    Parameters:
        graph (nx.Graph): A NetworkX graph.

    Returns:
        str: The digraph6 encoded string.
    """
    # Step 1: Compute N(n), the graph size character
    graph_size = graph.order()
    vertices = list(graph.nodes)

    if graph_size == 0:
        return ""  # empty graph
    elif graph_size == 1:
        return ""  # single-node graph

    N = chr(graph_size + 63)

    # Step 2: Compute R(x). Create bit vector from the upper triangle of the
    # adjacency matrix
    # For directed: read the matrix row by row
    bit_vector = []
    for r in vertices:
        for c in vertices:
            if graph.has_edge(r, c):
                bit_vector.append(1)
            else:
                bit_vector.append(0)

    # Step 3: Pad bit vector with zeros to make its length a multiple of 6
    while len(bit_vector) % 6 != 0:
        bit_vector.append(0)

    # Step 4: Convert each group of 6 bits to an ASCII character for encoding
    R = ""
    for i in range(0, len(bit_vector), 6):
        group = bit_vector[i : i + 6]
        group_value = sum((bit << (5 - idx)) for idx, bit in enumerate(group))
        R += chr(group_value + 63)

    return chr(38) + N + R

def toLabelg(label:str):
    label_g = "./labelg"  # Name of the executable
    # Check if the labelg executable exists in the root directory
    if os.path.isfile(label_g):
        os.chmod(label_g, 0o755)  # Ensure it is executable
    else:
        st.write("labelg exists: False")
        return

    try:
        result = subprocess.run(
            [label_g],
            input=label + "\n",
            text=True,
            capture_output=True,
            check=True,
        )

        #if subprocess runs correctly
        if result.returncode == 0:
            labelg_output = result.stdout
        else:
            st.write(
                "Subprocess failed with return code:",
                result.returncode,
            )
            st.error(result.stderr)

    except subprocess.CalledProcessError as e:
        st.write("error running labelg:")
        st.write(e.stderr)

    return labelg_output

def get_graph_label(nx_graph: nx.Graph, graph_type: GraphType) -> str:
    """
    Label a graph in either graph6 (undirected) or digraph6 (directed) format.
    """
    
    #for windows
    if graph_type == GraphType.UNDIRECTED:
        return graph6(nx_graph)
    if graph_type == GraphType.DIRECTED:
        return digraph6(nx_graph)
    
    '''
    #for linux
    if graph_type == GraphType.UNDIRECTED:
        return toLabelg(graph6(nx_graph))
    if graph_type == GraphType.DIRECTED:
        return toLabelg(digraph6(nx_graph))
    '''
