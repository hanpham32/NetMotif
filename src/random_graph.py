import networkx as nx

def generate_random_graphs(graph, number_of_graphs: int, graph_type): #graph must be networkx undireced or directed graph
    random_graphs = list()
    #random_graphs.append(1)
    #random_graphs.append(graph)
    if(graph_type == "Undirected"):
        a = nx.configuration_model(graph.degree(), nx.Graph())
        random_graphs.append(a)
    else:
        random_graphs.append(nx.configuration_model(graph.degree()), nx.DiGraph)
    #for i in range(number_of_graphs):
        #random_graphs.append(nx.configuration_model(graph.degree))
    return random_graphs
