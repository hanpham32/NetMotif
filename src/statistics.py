from typing import List
from graph_utils import Graph
import math

'''
keep in mind, graphs is a variable for a list of all graphs' subgraphs,
named, enumerated, and put into a dictionary
'''

#returns a dictionary of all stastical information for each unique label in graphs
def processStatistics(original_graph: Graph, graphs: list[Graph]):
    labelTable: dict = {} #label -> [frequency, mean, sd, zscore, p-value]
    generateListofAllUniqueLabels(graphs, labelTable)
    total_number_of_subgraphs = sum(original_graph.subgraph_list_enumerated.values())
    for label in labelTable:
        #labelTable[label][0] = graphs[label]
        mean = getLabelMean(label, graphs)
        labelTable[label][1] = mean / total_number_of_subgraphs # % mean-frequency
        sd = getStandardDeviation(mean, label, graphs)
        labelTable[label][2] = sd # standard deviation
        z_score = getZScore(sd, mean, label, original_graph)
        labelTable[label][3] = z_score # z-score
    return labelTable


'''
method written by ChatGPT
finds every unique key in a list of dictionaries and sets them as the
keys in second input dictionary
'''
def generateListofAllUniqueLabels(graphs: list[Graph], labelTable: dict):
    # Create an empty set to store unique keys
    unique_keys = set()

    # Iterate through each dictionary in the list
    for graph in graphs:
        # Add the keys of the current dictionary to the set
        labelTable.update(graph.subgraph_list_enumerated.keys())

    for key in unique_keys:
        labelTable[key] = {'mean': 0, 'sd': 0, 'z-score': 0, 'p-value': 0}

def getLabelMean(label, graphs: list[Graph]):
    totalCountOfMotif = 0
    for graph in graphs:
        if label in graph.subgraph_list_enumerated:
            totalCountOfMotif += graph.subgraph_list_enumerated[label]
    return totalCountOfMotif/len(graphs)

def getStandardDeviation(mean, label, graphs: list[Graph]):
    variance = 0
    for graph in graphs:
        if label in graph:
            xi = graph.subgraph_list_enumerated[label]
            variance += (xi-mean)**2
        else:
            variance += mean**2
    variance = variance/(len(graphs) - 1)
    return variance**0.5

def getZScore(sd: float, mean: float, label, original_graph: Graph):
    score = original_graph.subgraph_list_enumerated[label]
    return (score - mean)/sd

def _cdf(z:float):
    ''' cumaltive density function used for calculating p values '''
    return 0.5 * (1 + math.erf(z/math.sqrt(2)))

def getPValue(zscores: dict, label) -> dict:
    ''' Calculate the P value, using a 2-tail test, for each subgraph in the original graph using Z values'''
    #subtracting 1 from cdf value and multiplying result by 2 to get 2-tailed p value
    return 2*(1 - (_cdf(math.fabs(zscores[label]))))