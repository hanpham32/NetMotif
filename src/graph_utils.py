import networkx as nx
from io import StringIO
import matplotlib.pyplot as plt
import streamlit as st
from pyvis.network import Network


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

    def draw(self, graph_type):
        if graph_type == "Directed":
            nt = Network(directed=True)
        else:
            nt = Network()
        nt.from_nx(self.G)
        nt.toggle_physics(True)  # add physic to graph
        nt.toggle_hide_edges_on_drag(True)

        # Render the graph to an HTML file
        nt.write_html('nx.html', open_browser=False)
        with open("nx.html", "r") as f:
            html = f.read()
        st.components.v1.html(html, height=500)
