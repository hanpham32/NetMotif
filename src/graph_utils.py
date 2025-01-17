"""
Graph Class

This class is responsible for graph generation, visualization, and\
    rendering using NetworkX and Pyvis.

"""

from typing import List
import networkx as nx
import os
from io import StringIO
import streamlit as st
import streamlit.components.v1 as components
from streamlit.runtime.uploaded_file_manager import UploadedFile
from pyvis.network import Network
from src.esu import ESU
import src.labeling as labeling
import subprocess
from src.types import GraphType
from collections import defaultdict


class Graph:
    def __init__(self, graph_type, input, motif_size):
        self.graph_type = graph_type
        self.file = input
        self.motif_size = motif_size
        self.G = None
        self.esu = None

        # build graph
        if graph_type == GraphType.UNDIRECTED:
            self.G = nx.Graph()
        elif graph_type == GraphType.DIRECTED:
            self.G = nx.DiGraph()
        # if input is Graph or DiGraph handle differtly
        if isinstance(input, UploadedFile):
            if input is not None:
                bytes_data = StringIO(input.getvalue().decode("utf-8"))
                data = bytes_data.readlines()

                for line in data:
                    nodes = line.strip().split()
                    if len(nodes) == 2:
                        self.G.add_edge(nodes[0], nodes[1])
        else:
            self.G = input

        # enumerate subgraphs
        self.esu = ESU(self.G, motif_size)

    def get_graph_properties(self):
        if self.G is None:
            return {}

        return {
            "Number of nodes": self.G.number_of_nodes(),
            "Edges": list(self.G.edges()),
            "Number of edges": self.G.number_of_edges(),
            "Weight": self.G.size(),
        }

    def generate_random_graphs(self, number_of_graphs) -> List["Graph"]:
        random_graphs: List["Graph"] = []
        for i in range(number_of_graphs):
            if self.graph_type == GraphType.UNDIRECTED:
                degree_sequence = [d for _, d in self.G.degree()]
                random_graph = nx.Graph(nx.configuration_model(degree_sequence))
                random_graph = Graph(
                    input=random_graph,
                    graph_type=self.graph_type,
                    motif_size=self.motif_size,
                )
            elif self.graph_type == GraphType.DIRECTED:
                in_degree_sequence = [d for _, d in self.G.in_degree()]
                out_degree_sequence = [d for _, d in self.G.out_degree()]
                random_graph = nx.DiGraph(
                    nx.directed_configuration_model(
                        in_degree_sequence, out_degree_sequence
                    )
                )
                random_graph = Graph(
                    input=random_graph,
                    graph_type=self.graph_type,
                    motif_size=self.motif_size,
                )
            random_graphs.append(random_graph)
        for graph in random_graphs:
            graph.draw_graph()
        return random_graphs

    def draw_graph(self):
        output_dir = "drawings"
        if self.graph_type == GraphType.DIRECTED:
            nt = Network(directed=True)
        else:
            nt = Network()
        nt.from_nx(self.G)
        nt.toggle_physics(True)  # add physic to graph
        nt.toggle_hide_edges_on_drag(True)
        nt.show_buttons(filter_=["physics"])

        # Render the graph to an HTML file
        file_name = os.path.join(output_dir, "nx.html")

        # make sure output folder for the drawings exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        nt.write_html(file_name, open_browser=False)
        with open(file_name, "r") as f:
            html = f.read()

        components.html(html, height=1000, scrolling=True)

    def draw_subgraph(self, motif_size: int):
        output_dir = "drawings/subgraphs"  # output directory
        # make sure output folder for the drawings exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i, subgraph in enumerate(self.esu.get_subgraph_list()):
            if self.graph_type == GraphType.DIRECTED:
                nt = Network(directed=True)
            else:
                nt = Network()

            nt.from_nx(subgraph)
            file_name = os.path.join(output_dir, f"nx_subgraph_{i}.html")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            nt.write_html(file_name, open_browser=False)

            with open(file_name, "r") as f:
                html = f.read()

            st.markdown(
                f"### Subgraph {labeling.get_graph_label(subgraph, self.graph_type)}"
            )
            components.html(html, height=600, scrolling=True)
        return

    def print_labelg(self):
        """
        Takes in esu subgraph list and output the labels into a .txt file.
        """
        output_dir = "out"
        labels_file_output = os.path.join(output_dir, "labels.txt")

        # Ensure output folder exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        label_counter = defaultdict(int)

        # Convert to graph6 type
        with open(labels_file_output, "w") as file:
            for subgraph in self.esu.get_subgraph_list():
                label = labeling.get_graph_label(subgraph, self.graph_type)
                label_counter[label] += 1
                label = label + "\n"
                file.writelines(label)

        # Convert to labelg
        label_g = "./labelg"  # Name of the executable

        # Check if the labelg executable exists in the root directory
        if os.path.isfile(label_g):
            os.chmod(label_g, 0o755)  # Ensure it is executable
        else:
            st.write("labelg exists: False")
            return

        try:
            with open(labels_file_output, "r") as file:

                # Clear previous contents of the labelg output file
                labelg_output_file = os.path.join(output_dir, "labelg_output.txt")
                with open(labelg_output_file, "w") as labelg_file:
                    labelg_file.write("")

                for line in file:
                    line = line.strip()

                    result = subprocess.run(
                        [label_g],
                        input=line + "\n",
                        text=True,
                        capture_output=True,
                        check=True,
                    )

                    if result.returncode == 0:
                        labelg_output = result.stdout
                        labelg_output_file = os.path.join(
                            output_dir, "labelg_output.txt"
                        )
                        with open(labelg_output_file, "a") as labelg_file:
                            labelg_file.write(labelg_output + "\n")
                    else:
                        st.write(
                            "Subprocess failed with return code:",
                            result.returncode,
                        )
                        st.error(result.stderr)

            # after running all the inputs through labelg program, display the entire file
            # with open(labelg_output_file, "r") as labelg_file:
            st.subheader("Labelg Output")
            print(label_counter)
            for label, count in label_counter.items():
                st.text(f"{label}: {count}")

        except subprocess.CalledProcessError as e:
            st.write("error running labelg:")
            st.write(e.stderr)
