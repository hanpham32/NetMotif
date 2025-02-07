from src.graph_with_subgraph import GraphWithSubgraph
import math
import scipy.stats
import pandas as pd
import streamlit as st
#import streamlit.components.v1 as components

def draw_statistics(label_table: dict):
    motif_table: dict = {}
    #st.write(label_table.keys())
    for key in label_table.keys():
        new_key = ""
        new_key += key.get_label()
        #new_key += components.html(key.draw_graph())
        motif_table[new_key] = label_table[key]
    df = pd.DataFrame.from_dict(label_table, orient = 'index')
    st.table(df)

#returns a dictionary of all stastical information for each unique label in graphs
def process_statistics(original_graph: GraphWithSubgraph, graphs: list[GraphWithSubgraph]) -> dict:
    label_table: dict = {} #label -> [frequency, mean, sd, zscore, p-value]
    _generate_empty_label_table(original_graph, label_table)
    total_number_of_subgraphs = sum(original_graph.subgraph_list_enumerated.values())
    for label in label_table:
        if(label in original_graph.subgraph_list_enumerated):
            #frequency of label as a percent
            label_table[label]['freq'] = (original_graph.subgraph_list_enumerated[label]/total_number_of_subgraphs)*100
            st.write(label_table[label]['freq'])
        mean = _getLabelMean(label, graphs)
        label_table[label]['mean'] = mean * 100 # % mean-frequency as a percent
        sd = _getStandardDeviation(mean, label, graphs)
        label_table[label]['sd'] = sd # standard deviation
        z_score = _getZScore(sd, mean, label, original_graph)
        label_table[label]['z-score'] = z_score # z-score
        p_value = _getPValue(z_score)
        label_table[label]['p-value'] = p_value # p-value
    return label_table


'''
method written by ChatGPT
finds every unique key in a list of dictionaries and sets them as the
keys in second input dictionary
'''
def _generate_empty_label_table(graph: GraphWithSubgraph, label_table: dict):
    # Create an empty set to store unique keys
    unique_keys = set()

    # Add the keys of the current dictionary to the set
    unique_keys.update(graph.subgraph_list_enumerated.keys())

    for key in unique_keys:
        label_table[key] = {'freq': 0,'mean': 0, 'sd': 0, 'z-score': 0, 'p-value': 0}

def _getLabelMean(label, graphs: list[GraphWithSubgraph]):
    graph_frequency = 0
    frequencys = 0
    for graph in graphs:
        if label in graph.subgraph_list_enumerated:
            graph_frequency = graph.subgraph_list_enumerated[label]
            total_number_of_subgraphs = sum(graph.subgraph_list_enumerated.values())
            frequencys += graph_frequency/total_number_of_subgraphs
    return frequencys/len(graphs)

def _getStandardDeviation(mean, label, graphs: list[GraphWithSubgraph]):
    variance = 0
    for graph in graphs:
        if label in graph.subgraph_list_enumerated:
            xi = graph.subgraph_list_enumerated[label]
            variance += (xi-mean)**2
        else:
            variance += mean**2
    variance = variance/(len(graphs))
    return variance**0.5

def _getZScore(sd: float, mean: float, label, original_graph: GraphWithSubgraph):
    score = 0
    if(label in original_graph.subgraph_list_enumerated):
        score = original_graph.subgraph_list_enumerated[label]
    return (score - mean)/sd

def _getPValue(zscore: float):
    return scipy.stats.norm.sf(abs(zscore))*2
    ''' Calculate the P value, using a 2-tail test, for each subgraph in the original graph using Z values'''
    #subtracting 1 from cdf value and multiplying result by 2 to get 2-tailed p value
    return 2*(1 - (_cdf(math.fabs(std, zscore))))

'''
cumaltive density function used for calculating p values
def _cdf(z:float):
    return 0.5 * (1 + math.erf(z/((std)(2**0.5))))
'''