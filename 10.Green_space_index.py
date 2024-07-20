# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:46:43 2023

@author: Jiaqi Yao, Jingyu Duan

This file calculates the green space index
"""
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

community = load_variable('Data/community_income.txt')
green_space = load_variable('Data/green_space_ultimate.txt')
distance_matrix = load_variable('Data/distance_matrix_withcc.txt')

#####################################################################
'''
However, we notice that some of the green space are overlaped, which makes our analysis not accurate. 
Many of the green spaces are multi-use, but they all appear in the data.
So let's do one thing first:
count duplicate green spaces as one plot and record all the categories for each plot
'''

green_space_promax = pd.DataFrame(columns =green_space.columns )
green_space_promax['category'] = '' 

geo_set = set(green_space['area'])

for geo in geo_set:
    rows = green_space[green_space['area']==geo]
    
        
    if (isinstance(rows, pd.DataFrame)):
        if(len(rows)==1):
            row2 =rows.iloc[0,:]
            row2['category'] = row2['type']
            green_space_promax.loc[len(green_space_promax)] =row2
            
        else:
            index1 = np.argmax(np.array(rows['area']))
            row1 = rows.iloc[index1,:]
            
            row1['type'] = list(rows['type'])
            row1['category'] = 'multi_type'
            green_space_promax.loc[len(green_space_promax)] = row1
    
    elif (isinstance(rows, pd.Series)):
        green_space_promax.loc[len(green_space_promax)] = rows
        green_space_promax.iloc[len(green_space_promax)-1,:]['category'] = green_space_promax.iloc[len(green_space_promax)-1,:]['type']


green_space_promax = gpd.GeoDataFrame(green_space_promax)
save_variable(green_space_promax, 'Data/green_space_promax.txt')

#################################################################################
#All in all, calculate the green space index
green_index = pd.DataFrame(np.zeros((len(community),1))) #empty dataframe

green_index.index = community['SA2_NAME21']


for i in range(len(community)):
    com = community.iloc[i,:]['SA2_NAME21']
    
    for j in range(len(green_space_promax)):
        
        par = green_space_promax.iloc[j,:]['ogc_fid']
        par_data = green_space_promax.iloc[j,:]
        
        if (distance_matrix[com][par]!= np.inf):
            if (par_data['density'] != 0.0):
                a = par_data['area']/(math.exp(distance_matrix[com][par])*par_data['density'])
                green_index[0][com] +=a
                

save_variable(green_index,'Data/green_index.txt')

community['green_index'] = list(green_index[0])
community['log_index'] = list(np.log(green_index[0])) #we also calcualte the log of the index


#save data 
save_variable(community,'Data/community_ultimate.txt')

gdf1 = community.drop('geometry',axis = 1)
gdf1 = gdf1.drop('centroid',axis = 1)
gdf1.to_csv('Data/green_space_index.csv')
##################################################################################
'''
If you want to calculate the green sapce index of a certain type of green space, here is some code.
Take 'pos' as example
'''
# green_space = load_variable('Data/green_space_ultimate.txt')

# green_index_pos = pd.DataFrame(np.zeros((len(community),1)))
# green_index_pos.index = community['SA2_NAME21']

# green_space_pos = green_space[green_space['type']=='pos']


# for i in range(len(community)):
#     com = community.iloc[i,:]['SA2_NAME21']
    
#     for j in range(len(green_space_pos)):
        
#         par = green_space_pos.iloc[j,:]['ogc_fid']
#         par_data = green_space_pos.iloc[j,:]
        
#         if (distance_matrix[com][par]!= np.inf):
#             if (par_data['density'] != 0.0):
#                 a = par_data['area']/(math.exp(distance_matrix[com][par])*par_data['density'])
#                 green_index_pos[0][com] +=a
                

# save_variable(green_index_pos,'Data/green_index_pos.txt')

# community['green_index_pos'] = list(green_index_pos[0])
# community['log_index_pos'] = list(np.log(green_index_pos[0]))
