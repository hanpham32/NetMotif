from src.graph_utils import Graph
import src.label as lb
import streamlit as st

'''
A graph of same size as motif. GraphWithSubgraphs --<*> Subgraphs
'''
class Subgraph(Graph):
    label: str

    def __init__(self, graph_type, input):
        super().__init__(graph_type, input)  # Call the parent's __init__
        self.label = lb.get_graph_label(self.G, self.graph_type)

    def get_label(self):
        return self.label