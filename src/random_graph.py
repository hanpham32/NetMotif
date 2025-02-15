import networkx as nx
from src.graph_with_subgraph import GraphWithSubgraph
from src.graph_types import GraphType

def generate_random_graphs(mimicked_graph: GraphWithSubgraph, number_of_graphs) -> list[GraphWithSubgraph]:
    random_graphs: list[GraphWithSubgraph] = []
    for _ in range(number_of_graphs):
        random_graphs.append(generate_random_graph())
    return random_graphs

def generate_random_graph(mimicked_graph: GraphWithSubgraph):
    if mimicked_graph.graph_type == GraphType.UNDIRECTED:
            degree_sequence = [d for _, d in mimicked_graph.G.degree()]
            random_nx_graph = nx.Graph(nx.configuration_model(degree_sequence))
    elif mimicked_graph.graph_type == GraphType.DIRECTED:
        in_degree_sequence = [d for _, d in mimicked_graph.G.in_degree()]
        out_degree_sequence = [d for _, d in mimicked_graph.G.out_degree()]
        random_nx_graph = nx.DiGraph(
            nx.directed_configuration_model(
                in_degree_sequence, out_degree_sequence
            )
        )
    random_graph = GraphWithSubgraph(
        graph_type=mimicked_graph.graph_type,
        input=random_nx_graph,
        motif_size=mimicked_graph.motif_size,
    )
    return random_graph