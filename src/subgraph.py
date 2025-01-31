from src.graph_utils import Graph
import src.label as lb

'''
A graph of same size as motif. GraphWithSubgraphs --<*> Subgraphs
'''
class Subgraph(Graph):
    label: str

    def name(self):
        label = lb.get_graph_label(self.G, self.graph_type)


