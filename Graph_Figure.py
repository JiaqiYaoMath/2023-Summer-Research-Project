# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 15:47:49 2023

@author: LENOVO
"""
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

color_list=pd.read_csv('color_list.csv')

def select_color(color_list,n):
    i=0
    iteration=len(color_list)/n
    
    selected_color_list=[]
    
    for j in range(n):
        num=int(i+j*iteration)
        selected_color_list.append(color_list.iloc[num][0])    
    
    return selected_color_list
        

def Graph_Figure(G,C_list):
    #add attribute
    for key, value in C_list.items():
        for node in value:
            G.add_node(node,Group=key)
            
    #draw the graph
    n=len(C_list)
    selected_color_list=select_color(color_list,n)
    
    node_color_list=[]
    nodes=list(G.nodes)
    for node in nodes:
        group=G.nodes[node]['Group']
        group=group.strip('C')
        group=int(group)
        node_color_list.append(selected_color_list[group])
    
    nx.draw_networkx(G,node_color=node_color_list,edge_color='green' ,with_labels=True)
    plt.show()