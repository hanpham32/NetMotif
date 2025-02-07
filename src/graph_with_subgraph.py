import networkx as nx
import os
from io import StringIO
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
from src.graph_utils import Graph
from src.subgraph import Subgraph
from src.esu import ESU
from src.graph_types import GraphType

class GraphWithSubgraph(Graph):
    #simple list of all subgraphs generated by ESU algorithm
    subgraph_list: list[Subgraph] = []
    #dictionary of subgraph enumeration (Subgraph -> #)
    subgraph_list_enumerated: dict = {}
    #number of nodes in subgraphs
    motif_size: int = 0
    #esu object for esu algorithm
    esu = None

    def __init__(self, graph_type, input, motif_size):
        super().__init__(graph_type, input)
        self.motif_size = motif_size
        self.runESU(motif_size, graph_type)

    def runESU(self, motif_size, graph_type):
        # produce list of subgraphs
        self.esu = ESU(self.G, motif_size, graph_type)
        self.subgraph_list = self.esu.get_subgraph_list()
        # name and enumerate list of subgraphs
        self.enumerate_subgraphs()

    def enumerate_subgraphs(self):
        for subgraph in self.subgraph_list:
            #cur_label = subgraph.get_label()
            if subgraph not in self.subgraph_list_enumerated:
                self.subgraph_list_enumerated[subgraph] = 1
            else:
                self.subgraph_list_enumerated[subgraph] += 1
        #st.write(len(self.subgraph_list_enumerated))

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
