from src.graph_utils import Graph
from src.types import GraphType
import src.statistics as stat
import src.random_graph as rg

def main():
    basicGraph = Graph(GraphType.UNDIRECTED, "./data/basicTest.txt", 3)
    random_graphs = rg.generate_random_graphs(basicGraph, 10)
    # make a table of data for each label
    table = stat.processStatistics(basicGraph, random_graphs)
    print(table)