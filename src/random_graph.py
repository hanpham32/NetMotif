import networkx as nx
from src.graph_utils import Graph
from src.graph_types import GraphType

def generate_random_graphs(mimicked_graph: Graph, number_of_graphs) -> list["Graph"]:
    random_graphs: list["Graph"] = []
    for i in range(number_of_graphs):
        if mimicked_graph.graph_type == GraphType.UNDIRECTED:
            degree_sequence = [d for _, d in mimicked_graph.G.degree()]
            random_graph = nx.Graph(nx.configuration_model(degree_sequence))
            random_graph = Graph(
                input=random_graph,
                graph_type=mimicked_graph.graph_type,
                motif_size=mimicked_graph.motif_size,
            )
        elif mimicked_graph.graph_type == GraphType.DIRECTED:
            in_degree_sequence = [d for _, d in mimicked_graph.G.in_degree()]
            out_degree_sequence = [d for _, d in mimicked_graph.G.out_degree()]
            random_graph = nx.DiGraph(
                nx.directed_configuration_model(
                    in_degree_sequence, out_degree_sequence
                )
            )
            random_graph = Graph(
                input=random_graph,
                graph_type=mimicked_graph.graph_type,
                motif_size=mimicked_graph.motif_size,
            )
        random_graphs.append(random_graph)
    return random_graphs