
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 19:38:10 2023

@author: Jiaqi Yao, Jingyu Duan

This file tries to find the central vertex of each community.
Since the centroid of community is not vertex in network, we try to find the nearest vertex in network.
"""

#Packages
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable
from shapely.geometry import Polygon
from shapely.geometry import Point
import copy
from geopy.distance import geodesic

#Load data
community = load_variable('Data/community_centroid.txt')
adelaide_network = load_variable('Data/adelaide_network_community.txt')
###############################################
#find nearest node
central_nodes = [] #store central nodes as list
cc_walk = [] #We also store the distance between the centroid and the central nodes


for i in range(len(community)):
    centroid = community.iloc[i,:]['centroid']
    y = centroid.y
    x = centroid.x
    
    #select all the nodes in one community and set it as a subgraph
    selected_nodes = [node for node, data in adelaide_network.nodes(data=True) if 'Community' in data and data['Community'] == community.iloc[i,:]['SA2_NAME21']]
    subgraph = adelaide_network.subgraph(selected_nodes)
    
    #Find the nearest node in network
    central_node = ox.distance.nearest_nodes(subgraph, x, y)  
    central_nodes.append(central_node)
    
    y1 = adelaide_network.nodes[central_node]['y']
    x1 = adelaide_network.nodes[central_node]['x']
    
    #find the dsitance between two points
    dis = geodesic((y,x), (y1,x1)).meters #the unit of length is meter.
    
    cc_walk.append(dis)
    

community['central'] = central_nodes
cc_walk = np.array(cc_walk)/1000 #Set the unit of length as km


#Save data
save_variable(community,'Data/community_centroid.txt')
save_variable(cc_walk,'Data/cc_walk.txt')

