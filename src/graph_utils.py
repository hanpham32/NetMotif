"""
Graph Class

This class is responsible for graph generation, visualization, and\
    rendering using NetworkX and Pyvis.

"""

import networkx as nx
import os
from io import StringIO
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
from src.esu import ESU


class Graph:
    def __init__(self):
        self.G = None

    def generate_graph(self, file, graph_type):
        if graph_type == "Undirected":
            self.G = nx.Graph()
        elif graph_type == "Directed":
            self.G = nx.DiGraph()

        if file is not None:
            bytes_data = StringIO(file.getvalue().decode("utf-8"))
            data = bytes_data.readlines()

            for line in data:
                nodes = line.strip().split()
                if len(nodes) == 2:
                    self.G.add_edge(nodes[0], nodes[1])

        return self.G

    def graph_properties(self):
        if self.G is None:
            return {}

        return {
            "Number of nodes": self.G.number_of_nodes(),
            "Edges": list(self.G.edges()),
            "Number of edges": self.G.number_of_edges(),
            "Weight": self.G.size(),
        }

    def draw_graph(self, graph_type):
        output_dir = "drawings"
        if graph_type == "Directed":
            nt = Network(directed=True)
        else:
            nt = Network()
        nt.from_nx(self.G)
        nt.toggle_physics(True)  # add physic to graph
        nt.toggle_hide_edges_on_drag(True)
        nt.show_buttons(filter_=['physics'])

        # Render the graph to an HTML file
        file_name = os.path.join(output_dir, 'nx.html')
        nt.write_html(file_name, open_browser=False)
        with open(file_name, "r") as f:
            html = f.read()

        components.html(html, height=1000, scrolling=True)

    def draw_subgraph(self, graph_type: str, motif_size: int):
        output_dir = "drawings/subgraphs"
        esu = ESU(self.G)
        esu_list = esu.enumerate_subgraphs(motif_size)  # FIXME: 3 is default motif size

        for i, subgraph in enumerate(esu_list):
            if graph_type == "Directed":
                nt = Network(directed=True)
            else:
                nt = Network()

            nt.from_nx(subgraph)
            file_name = os.path.join(output_dir, f'nx_subgraph_{i}.html')
            nt.write_html(file_name, open_browser=False)

            with open(file_name, "r") as f:
                html = f.read()

            st.markdown(f"### Subgraph {i + 1}")
            components.html(html, height=600, scrolling=True)
        return
