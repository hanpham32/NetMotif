from src.graph_utils import Graph
from src.graph_types import GraphType
#import src.label as lb
#import streamlit as st
#import time

'''
A graph of same size as motif. GraphWithSubgraphs --<*> Subgraphs
'''
class Subgraph(Graph):
    #label_conversion_map: dict = {}

    def __init__(self, graph_type, input):
        super().__init__(graph_type, input)  # Call the parent's __init__
        self.label = ""
        #self.set_label()

    def __eq__(self, other):
        if isinstance(other, Subgraph):
            return self.label == other.label
        else:
            return False

    def __hash__(self):
        return hash(self.label)

    def get_label(self):
        return self.label

    def set_label(self, input_label):
        self.label = input_label
