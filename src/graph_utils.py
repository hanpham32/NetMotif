import networkx as nx
from io import StringIO


def graph_generation(uploaded_file):
    G = nx.Graph()

    if uploaded_file is not None:
        bytes_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = bytes_data.readlines()

        for line in data:
            nodes = line.strip().split()
            if len(nodes) == 2:
                G.add_edge(nodes[0], nodes[1])

    return G
