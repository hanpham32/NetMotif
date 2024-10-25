import networkx as nx

def g6Label(graph: nx.Graph):
    #motifSize = n
    graphSize = graph.order()

    #first figure out the N(n)
    N = chr(graphSize+63)

    #find x
    x = []
    diagonalCount: int
    columnCount = graphSize
    for c in graph:
        diagonalCount = 0
        for r in graph:
            if(diagonalCount<graphSize-columnCount):
                x.append(graph.has_edge(r, c))
            else: break
            diagonalCount = diagonalCount+1
        columnCount = columnCount-1

    #attach 0's until x length is multiple of 6
    while(len(x)%6 != 0):
        x.append(0)

    #convert x into its ascii character to get R(x)
    R = ""
    rCharList = [1] * int(len(x)/6)
    i = 0
    while(i < len(x)):
        rCharList[int(i/6)] = (rCharList[int(i/6)] << 1) | x[i]
        if(i%6 == 5):
            rCharList[int(i/6)] = rCharList[int(i/6)] - 1
        i = i + 1
    for element in rCharList:
        R = R + chr(element)
    #return(g6LabelCanonization(graph, N + R))
    return(N+R)

def d6Label(graph: nx.DiGraph):
    #motifSize = n
    graphSize = graph.order()

    #first figure out the N(n)
    N = chr(graphSize+63)

    #find x
    x = []
    for r in graph:
        for c in graph:
            x.append(graph.has_edge(r, c))

    #attach 0's until x length is multiple of 6
    while(len(x)%6 != 0):
        x.append(0)

    #convert x into its ascii character to get R(x)
    R = ""
    rCharList = [1] * int(len(x)/6)
    i = 0
    while(i < len(x)):
        rCharList[int(i/6)] = (rCharList[int(i/6)] << 1) | x[i]
        if(i%6 == 5):
            rCharList[int(i/6)] = rCharList[int(i/6)] - 1
        i = i + 1
    for element in rCharList:
        R = R + chr(element)
    #return(g6LabelCanonization(graph, N + R))
    return(N+R)

def labelGraph(networkx_graph, graph_type): #networkx di or undi graph
    if(graph_type == "Undirected"):
        return g6Label(networkx_graph)
    if(graph_type == "Directed"):
        return d6Label(networkx_graph)