#translated for networkx from https://github.com/IlyaVasUW/NEMO_SUITE/


#import networkx as nx
import src.graph_utils as gu
from io import StringIO
#import streamlit as st
#import streamlit.components.v1 as components
#from pyvis.network import Network
#from src.graph import UndirectedGraph
#from src.motif import Motif

def esu(graph: gu.Graph, size: int):
    #creates a list to hold all subgraph arrays
    subgraphList = list()
    #collects all starting nodes for search
    nodes = graph.G.nodes()

    #loops through every starting node and enters a recursive function to find subgraphs for each
    nodeVisited = set()
    for node in nodes:
        #neighbors is a set so that adding new values in the future will be easier
        neighborSet = set(graph.getRightNeighbors(node))
        #creates the start of a subgraph
        nodeList = [node]
        nodeVisited.add(node)
        esu_recurse(graph, size, neighborSet, nodeList, subgraphList, nodeVisited)

    return subgraphList


def esu_recurse(graph: gu.Graph, size: int, neighbors: set,
                nodeList: list, subgraphList: list, nodesVisited: set):

    #if subgraph is complete
    if size == 1:
        subgraphList.append(nodeList.copy())
        return

    #checks if there are no more neighbors to pull from
    elif len(neighbors) == 0:
        return

    #recurses for every neighbor
    for node in neighbors:
        #add node to the current subgraph list
        nodeList.append(node)
        nodesVisited.add(node)
        nextNeighbors = set()

        #only adds nodes that have not been visited to the next neighbors list
        for neighbor in neighbors:
            if neighbor not in nodesVisited:
                nextNeighbors.add(neighbor)
        for neighbor in graph.G.neighbors(node):
            if neighbor not in nodesVisited:
                nextNeighbors.add(neighbor)

        #sends the neighbors list for the next node to the recursion
        esu_recurse(graph, size-1, nextNeighbors, nodeList, subgraphList, nodesVisited)

        #this removes the previously searched node from the current subgraph list
        if len(nodeList) > 0:
            nodeList.pop()

    #if the nodes been visited, it is removed from the neighbor set
    for node in neighbors:
        nodesVisited.discard(node)

"""
def esuGraph(graph: gu.Graph, size: int):
    motifNodes = esu(graph, size)
    for nodes in motifNodes:
        Motif(nodes, graph)
"""