# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:43:02 2024

@author: Jiaqi Yao, Jingyu Duan

This file finds the distance between green space and SA2
"""

#Load package
import geopandas as gpd
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable
from shapely.geometry import Polygon
from shapely.geometry import Point
from geopy.distance import geodesic
from pyproj import Geod
import copy
import math
import geopandas as gpd

#Load data
adelaide_network = load_variable('Data/adelaide_network_community_color.txt')
G = nx.Graph(adelaide_network )
cc_walk = load_variable('Data/cc_walk.txt')
green_space = load_variable('Data/green_space_ultimate.txt')
community = load_variable('Data/community_income.txt')

#############################################################################################
#Distance
#Notice! in this matrix, the element of ith row, jth column is the distance from j to i

#######################################################################################communication
#Find the green space where each node is located
for node1 in list(adelaide_network.nodes):
    adelaide_network.add_node(node1,Green='None') #first assign none to each node


polygon_nolist = [] #store the set of nodes owned by each green space

for i in range(len(green_space)):
    polygon = green_space.iloc[i,:]['geometry']
    
    nodes_in_polygon = [node for node, data in adelaide_network.nodes(data=True) if Point(data["x"], data["y"]).within(polygon)]
    polygon_nolist.append(nodes_in_polygon)



save_variable(polygon_nolist,'Data/polygon_nolist2.txt')


######################################################################################
#For some green space, there are no network nodes in it. Find its nearest network node and the distance.

extra_walk = [] #distance to its nearest node

for i in range(len(green_space)):
    if (polygon_nolist[i]==[]):
        polygon = green_space.iloc[i,:]['geometry']
        centroid = polygon.centroid
        y = centroid.y
        x = centroid.x
        
        nearest_node = ox.distance.nearest_nodes(adelaide_network, x, y)
        polygon_nolist[i].append(nearest_node)
        
        y1 = adelaide_network.nodes[nearest_node]['y']
        x1 = adelaide_network.nodes[nearest_node]['x']
        
        dis = geodesic((y,x), (y1,x1)).meters
        extra_walk.append(dis)
    else:
        extra_walk.append(0) #if there are nodes in green space, the distance is 0.

save_variable(polygon_nolist,'Data/polygon_nolist3.txt')
save_variable(extra_walk,'Data/extra_walk.txt')

save_variable(adelaide_network,'Data/adelaide_network_green.txt')
############################################################
#create the distance matrix
#Notice! in this matrix, the element of ith row, jth column is the distance from j to i

matrix = np.zeros((len(green_space),len(community)))
matrix2 = pd.DataFrame(matrix) 
distance_matrix = matrix2


distance_matrix.index = green_space['ogc_fid']
distance_matrix.columns = community['SA2_NAME21']

#########################################################################
#A function to find the distances from one node to all green spaces
#Output is a vector
def node_to_region_length(G,node,green_space):
    dis_list = np.ones((len(green_space),1))*np.inf
    dis_ser = pd.DataFrame(dis_list)
    dis_ser.index = list(green_space['ogc_fid'])
    dis_ser.columns = list('1')
    
    
    all_dis = nx.shortest_path_length(G, node, weight='length')
    
    
    for k in range(len(dis_ser)):
        nodes = polygon_nolist[k]
        name = green_space.iloc[k,:]['ogc_fid']
        
        for node3 in nodes:
            if(all_dis[node3]<dis_ser['1'][name]):
                dis_ser['1'][name] = all_dis[node3]
     
    for i in range(len(dis_ser)):
        dis_ser.iloc[i,:]['1']+= extra_walk[i]
    return dis_ser


#use the function to find the distances from each central node
for index1 in community['SA2_NAME21']:
    com = community[community['SA2_NAME21']==index1]
    node = int(com['central'].iloc[0])
    dis_ser = node_to_region_length(G,node,green_space)
    
    for index2 in green_space['ogc_fid']:
        distance_matrix[index1][index2] = dis_ser['1'][index2]

#km as unit
distance_matrix = distance_matrix/1000
save_variable(distance_matrix,'Data/distance_matrix.txt')


############################################################
#The version that add the distance between centroid and central node
distance_matrix_withcc = copy.deepcopy(distance_matrix)


for i in range(len(distance_matrix)):
    for j in range(len(distance_matrix.columns)):
        distance_matrix_withcc.iloc[i,j]+=cc_walk[j]


save_variable(distance_matrix_withcc,'Data/distance_matrix_withcc.txt')
