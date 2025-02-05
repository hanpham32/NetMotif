from src.graph_utils import Graph
import src.label as lb

'''
A graph of same size as motif. GraphWithSubgraphs --<*> Subgraphs
'''
class Subgraph(Graph):
    label: str

    def __init__(self, graph_type, input, motif_size):
        super().__init__(self, graph_type, input, motif_size)  # Call the parent's __init__
        self.label = self.setLabel()

    def setLabel(self):
        self.label = lb.get_graph_label(self.G, self.graph_type)

    def get_label(self):
        return self.label