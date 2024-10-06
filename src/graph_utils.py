import networkx as nx
from io import StringIO
import matplotlib.pyplot as plt
import streamlit as st


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

    def draw(self, draw_option):
        plt.figure(figsize=(8, 6))
        match draw_option:
            case "Spring Layout":
                nx.draw_spring(self.G)
            case "Circular Layout":
                nx.draw_circular(self.G)
            case "Planar Layout":
                nx.draw_planar(self.G)
            case _:
                pos = nx.spring_layout(self.G)
                nx.draw(self.G, pos)

        st.pyplot(plt.gcf())
