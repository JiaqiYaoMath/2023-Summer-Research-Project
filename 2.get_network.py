# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:53:01 2023

@author: Jiaqi Yao, Jingyu Duan

This file is used to collect and store data on network of Adelaide
"""

#Packages
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable

		
#community data
community = load_variable('Data/community.txt')


# Set the latitude and longitude range for the map area
north, south, east, west = -34.3, -35.68, 139.25, 138.05

# get network from OSMnx
G = ox.graph_from_bbox(north, south, east, west, network_type='all')
G1 = nx.Graph(G)


#plot the map
fig, ax = ox.plot_graph(G)


# save the map
save_variable(G,'Data/adelaide_network.txt')
save_variable(G1,'Data/adelaide_network_graph.txt')
#why the edges in walk network is more than in all network?