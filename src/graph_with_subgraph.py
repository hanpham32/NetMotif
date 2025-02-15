import networkx as nx
import os
from io import StringIO
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
from tabulate import tabulate
from src.graph_utils import Graph
from src.subgraph import Subgraph
from src.esu import ESU
from src.graph_types import GraphType

class GraphWithSubgraph(Graph):
    def __init__(self, graph_type, input, motif_size):
        #simple list of all subgraphs generated by ESU algorithm
        self.subgraph_list: list[Subgraph] = []
        #dictionary of subgraph enumeration (Subgraph -> #)
        self.subgraph_list_enumerated: dict = {}
        #number of nodes in subgraphs
        self.motif_size: int = 0
        #esu object for esu algorithm
        self.esu = None

        #instantiation of Graph object
        super().__init__(graph_type, input)
        #setting motif size
        self.motif_size = motif_size
        #creating Subgraph list and dict
        self.runESU(motif_size, graph_type)

    def runESU(self, motif_size, graph_type):
        # produce list of subgraphs
        self.esu = ESU(self.G, motif_size, graph_type)
        self.subgraph_list = self.esu.get_subgraph_list()
        # name and enumerate list of subgraphs
        self.enumerate_subgraphs()

    def enumerate_subgraphs(self):
        for subgraph in self.subgraph_list:
            if subgraph not in self.subgraph_list_enumerated:
                self.subgraph_list_enumerated[subgraph] = 1
            else:
                self.subgraph_list_enumerated[subgraph] += 1

    def draw_subgraph(self):
        output_dir = "drawings/subgraphs"  # output directory
        # make sure output folder for the drawings exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i, subgraph in enumerate(self.subgraph_list):
            if self.graph_type == GraphType.DIRECTED:
                nt = Network(directed=True)
            else:
                nt = Network()

            nt.from_nx(subgraph.G)
            file_name = os.path.join(output_dir, f"nx_subgraph_{i}.html")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            nt.write_html(file_name, open_browser=False)

            with open(file_name, "r") as f:
                html = f.read()

            st.markdown(
                f"### Subgraph {subgraph.get_label()}"
            )
            components.html(html, height=600, scrolling=True)
        return

        #@st.cache_data
    def generate_subgraph_profile(self):
        output_dir = "out"
        subgraph_profile_output = os.path.join(output_dir, "subgraph_profile.csv")

        # Ensure output folder exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        #label-node count dictionary
        nodes_dictionary = {}
        
        #iterate over subgraphs
        for subgraph in self.subgraph_list:
            label = subgraph.get_label()
            #if label not accounted for
            if label not in nodes_dictionary:
                #fill in all node count as 0 for label
                nodes_dictionary[label] = {}
                for node in self.G:
                    nodes_dictionary[label][node] = 0
            #for every node in the subgraph add 1 to its label-node count
            for node in subgraph.G.nodes:
                nodes_dictionary[label][node] += 1
    
        #table to show profile for each node-label count
        df = pd.DataFrame.from_dict()

        table = tabulate(df, headers='keys', tablefmt='grid', showindex=False)

        # Convert DataFrame to CSV
        csv = df.to_csv(subgraph_profile_output)

        #Display download button for dataframe
        return st.download_button(
            label="Download subgraph profile",
            data=csv,
            file_name="subgraph_profile.txt",
            mime="text/csv"
        )

    #@st.cache_data
    def generate_subgraph_collection(self):
        output_dir = "out"
        subgraph_collection_output = os.path.join(output_dir, "subgraph_collection.txt")

        # Ensure output folder exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write into file
        with open(subgraph_collection_output, "w") as file:
            for subgraph in self.subgraph_list:
                nodes = subgraph.G.nodes()
                line = ""
                line += subgraph.get_label() + "\n[" + ", ".join([str(x) for x in nodes]) + "] \n"
                file.writelines(line)

        #Display download button for file
        with open(subgraph_collection_output, "r") as file:
            return st.download_button(
                label="Download subgraph collection",
                data=file,
                file_name="subgraph_collection.txt",
            )