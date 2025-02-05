import networkx as nx
from src.graph_with_subgraph import GraphWithSubgraph
from src.graph_types import GraphType

def generate_random_graphs(mimicked_graph: GraphWithSubgraph, number_of_graphs) -> list["GraphWithSubgraph"]:
    random_graphs: list["GraphWithSubgraph"] = []
    for i in range(number_of_graphs):
        if mimicked_graph.graph_type == GraphType.UNDIRECTED:
            degree_sequence = [d for _, d in mimicked_graph.G.degree()]
            random_graph = nx.Graph(nx.configuration_model(degree_sequence))
        elif mimicked_graph.graph_type == GraphType.DIRECTED:
            in_degree_sequence = [d for _, d in mimicked_graph.G.in_degree()]
            out_degree_sequence = [d for _, d in mimicked_graph.G.out_degree()]
            random_graph = nx.DiGraph(
                nx.directed_configuration_model(
                    in_degree_sequence, out_degree_sequence
                )
            )
        random_graph = GraphWithSubgraph(
            input=random_graph,
            graph_type=mimicked_graph.graph_type,
            motif_size=mimicked_graph.motif_size,
        )
        random_graphs.append(random_graph)
    return random_graphs