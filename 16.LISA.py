# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:33:01 2023

@author: 23783
"""
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
from sklearn import preprocessing

community = load_variable('Data/community_ultimate.txt')

########################################################################################
##Create adjacency matrix
matrix = np.zeros((len(community),len(community)))
matrix2 = pd.DataFrame(matrix) 
adjacency_matrix = matrix2

index = community['SA2_NAME21']
adjacency_matrix.index = index
adjacency_matrix.columns = index


#plot the polygon
#polygon1.plot()

#fill up the adjacency_matrix
for index1 in index:
    for index2 in index:
        polygon1 =   community[community['SA2_NAME21']==index1]
        polygon2 =   community[community['SA2_NAME21']==index2]
        
        geo1 = polygon1['geometry'].iloc[0]
        geo2 = polygon2['geometry'].iloc[0]
        
        indicator = int(geo1.intersects(geo2))
        adjacency_matrix[index1][index2] = indicator

#for diagnoal elements, zero
for i in range(len(index)):
    adjacency_matrix.iloc[i,i] = 0

adj = np.matrix(adjacency_matrix).astype(int)


##################################################################################33

def adjacency_matrix_to_weight_matrix(adjacency_matrix):
    # Get the number of rows (number of nodes) of the matrix
    num_nodes = len(adjacency_matrix)
    
    # Create an empty adjacency weight matrix
    weight_matrix = np.zeros((num_nodes, num_nodes))
    
    # Iterate over each line
    for i in range(num_nodes):
        # Calculate the sum of the non-zero elements of the current line
        row_sum = adjacency_matrix[i,:].sum()
        
        # Keep the current row of the weight matrix zero if the sum of the non-zero elements in the current row is zero
        if row_sum == 0:
            weight_matrix[i] = np.zeros(num_nodes)
        else:
            # Calculate the current row of the neighbor weight matrix
            weight_matrix[i] = adjacency_matrix[i] / row_sum
    
    return weight_matrix

wei = adjacency_matrix_to_weight_matrix(adj)


########################################################################
income = np.array(community['Median'])
green = np.array(community['green_index'])

st_green = preprocessing.scale(green)
st_income = preprocessing.scale(income)

a = wei @ st_green
I = st_income * a

np.mean(I)
