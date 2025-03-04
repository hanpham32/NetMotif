import networkx as nx
import streamlit as st
from src.graph_with_subgraph import GraphWithSubgraph
from src.graph_types import GraphType

def generate_random_graphs(mimicked_graph: GraphWithSubgraph, number_of_graphs) -> list[GraphWithSubgraph]:
    progress_text = "Random graph generation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    random_graphs: list[GraphWithSubgraph] = []
    for i in range(number_of_graphs):
        random_graphs.append(generate_random_graph(mimicked_graph))
        my_bar.progress(i/st.session_state['number_of_random_graphs'], text=progress_text)
    my_bar.empty()
    return random_graphs

def generate_random_graph(mimicked_graph: GraphWithSubgraph):
    progress_text = "Generating one graph generation. Please wait."
    my_bar = st.progress(0, text=progress_text)
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
    my_bar = st.progress(0.5, text=progress_text)
    random_graph = GraphWithSubgraph(
        graph_type=mimicked_graph.graph_type,
        input=random_nx_graph,
        motif_size=mimicked_graph.motif_size,
    )
    my_bar = st.progress(1, text=progress_text)
    my_bar.empty()
    return random_graph