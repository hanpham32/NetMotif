from src.graph_utils import Graph
from src.graph_types import GraphType
import src.label as lb
import streamlit as st

'''
A graph of same size as motif. GraphWithSubgraphs --<*> Subgraphs
'''
class Subgraph(Graph):
    label_conversion_map: dict = {}

    def __init__(self, graph_type, input):
        super().__init__(graph_type, input)  # Call the parent's __init__
        self.label = ""
        self.set_label()

    def __eq__(self, other):
        if isinstance(other, Subgraph):
            return self.label == other.label
        return False

    def __hash__(self):
        return hash(self.label)

    def get_label(self):
        return self.label
    
    def set_label(self):
        if self.graph_type == GraphType.UNDIRECTED:
            basic_label = lb.graph6(self.G)
        elif self.graph_type == GraphType.DIRECTED:
            basic_label = lb.digraph6(self.G)
        if basic_label not in Subgraph.label_conversion_map:
            Subgraph.label_conversion_map[basic_label] = lb.get_graph_label(self.G, self.graph_type)
        self.label = Subgraph.label_conversion_map[basic_label]
            