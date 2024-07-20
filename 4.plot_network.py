# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:17:56 2023

@author: Jiaqi Yao, Jingyu Duan

This document is intended to plot Adelaide's transportation network,
but it has no relevance to the work that follows
"""

#Load packages
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable
from  Graph_Figure import select_color
from shapely.geometry import Polygon
from shapely.geometry import Point
import contextily as ctx

#read variable
community = load_variable('Data/community_centroid.txt')
adelaide_network = load_variable('Data/adelaide_network.txt')
color_list=pd.read_csv('color_list.csv') #this file stores the name of all colors in Pyplot, it could be found in this file. 

###############################################################
'''
The following code attempts to communityize the nodes in the network:
the nodes are categorized according to the SA2 region in which they are located
'''

#Start by having each node's community property set to none
for node1 in list(adelaide_network.nodes):
    adelaide_network.add_node(node1,Community='None')


#If one node is located in a SA2 polygon, assign its community attribute to be that SA2
for node1 in list(adelaide_network.nodes):
    y = adelaide_network.nodes[node1]['y'] #find the loaction of the node
    x = adelaide_network.nodes[node1]['x']
    
    location = Point(x,y)
    
    for i in range(len(community)):
        polygon = community.iloc[i,:]['geometry']
        
        if (location.within(polygon)): #Determine if a node is in a region
            adelaide_network.add_node(node1,Community=community.iloc[i,:]['SA2_NAME21'])
            break


#If the community attribute of one node is none, try to find if It is close to an SA, i.e. at the edge of the SA region
#0.0015 in latitude and longitude coordinates equals approximately 100 meters.
for node1 in list(adelaide_network.nodes):
    if (adelaide_network.nodes[node1]['Community']=='None'):
        y = adelaide_network.nodes[node1]['y']  #find the loaction of the node
        x = adelaide_network.nodes[node1]['x']
        point = Point(x,y)
        Dis = 999999999999999999
        com = 'None'
        for i in range(len(community)):
            polygon = community.iloc[i,:]['geometry']
            dis1 = point.distance(polygon) #the dsitance between the node and a region
            
            if (dis1<=0.0015):  #Determine if a node is at the edge of one region
                if (dis1<Dis):  #If a node is at the edge of both regions, it belongs to the closer region
                    Dis = dis1
                    com = community.iloc[i,:]['SA2_NAME21']
        
        
        adelaide_network.add_node(node1,Community=com)


#Save network with community attribute
save_variable(adelaide_network,'Data/adelaide_network_community.txt')


################################################################
#Store the nodes owned by each community in a dictionary

#create a empty dict
C_list={}
for i in range(len(community)):
    C_list[community.iloc[i,:]['SA2_NAME21']]=[]
    C_list['None'] = []

#Assign the nodes owned by each community to the dict
for node2 in list(adelaide_network.nodes):
    C_list[adelaide_network.nodes[node2]['Community']].append(node2)


#Find a unique color for each community
#The select_color file is used to find a unique color for every single community, which can be checked in file: Graph_Figure.py
n=len(C_list)
selected_color_list=select_color(color_list,n)

#Save the color attribute in the network variable
for node2 in list(adelaide_network.nodes):
    community1 = adelaide_network.nodes[node2]['Community']
    
    if (community1 == 'None'):
        color = selected_color_list[105] #For nodes that does not belong to a community, assgin a unique color to them
    else:
        indexing = community.loc[community['SA2_NAME21'] == community1].index[0]
        color = selected_color_list[indexing]
        
    adelaide_network.add_node(node2,node_color = color)


save_variable(adelaide_network,'Data/adelaide_network_community_color.txt')

#################################################################
#Each edge has the same color as its source node
edge_colors = []
for edge in adelaide_network.edges:
    starting_node = edge[0]
    adelaide_network.edges[edge]['color'] = adelaide_network.nodes[starting_node]['node_color']
    edge_colors.append(adelaide_network.nodes[starting_node]['node_color'])



##################################################################
#convert the data structure of network
gvf, gdf = ox.graph_to_gdfs(adelaide_network, nodes=True, edges=True)
node_color_attribute = 'node_color'
edge_color_attribute = 'color'


# Get the color attribute of the node
node_colors = [adelaide_network.nodes[node][node_color_attribute] for node in adelaide_network.nodes()]
####################################################################
#plot the network


#set style
plt.style.use('seaborn-whitegrid')

fig, ax1 = plt.subplots(figsize=(12, 12))

gvf.plot(ax=ax1, color=node_colors, markersize=0)
gdf.plot(ax=ax1, color=edge_colors, linewidth=0.5)
ctx.add_basemap(ax=ax1 ,crs=gdf.crs.to_string())
fig.savefig('figure/road_network.pdf')

plt.show()
