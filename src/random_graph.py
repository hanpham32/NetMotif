import networkx as nx

def generate_random_graphs(graph, number_of_graphs: int, graph_type): #graph must be networkx undireced or directed graph
    random_graphs = list()
    for i in range(number_of_graphs):
        if(graph_type == "Undirected"):
            degree_sequence = [d for _, d in graph.degree()]
            random_graphs.append(nx.Graph(nx.configuration_model(degree_sequence)))
        elif(graph_type == "Directed"):
            in_degree_sequence = [d for _, d in graph.in_degree()]
            out_degree_sequence = [d for _, d in graph.out_degree()]
            random_graphs.append(nx.DiGraph(nx.directed_configuration_model(in_degree_sequence, out_degree_sequence)))
    return random_graphs
