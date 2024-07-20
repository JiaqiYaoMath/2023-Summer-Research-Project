# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 11:23:37 2023

@author: Jiaqi Yao, Jingyu Duan

This file gives a visualisation of green space index of SA2
"""

#package
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable
from shapely.geometry import Polygon
from shapely.geometry import Point
import contextily as ctx
from matplotlib.colors import LogNorm


#data
gdf = load_variable('Data/community_ultimate.txt')
cc = gdf['green_index']



#style
plt.style.use('seaborn-whitegrid')

min1 = np.min(np.array(cc))
max1 = np.max(np.array(cc))



########################################################################
#plot
c = gdf.plot( column='green_index', cmap='viridis', legend=True, figsize=(8,6),norm=LogNorm(vmin=min1, vmax=max1))
ctx.add_basemap(c ,crs=gdf.crs.to_string(),source=ctx.providers.OpenStreetMap.France)


# cbar = plt.colorbar(c.get_children()[0], ax=c, location = 'top', pad=0.05,shrink=0.8)

# # Rotate the label text on the color bar
# cbar.ax.set_xticklabels(cbar.ax.get_xticklabels(), rotation=90)

#plt.title('Log Green Space Index In Greater Adelaide by Statistical Area 2',  fontdict={'fontname': 'Times New Roman', 'fontsize': 20})
plt.xlabel('Longitude', fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
plt.ylabel('Latitude', fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
# plt.xticks(rotation=90)
# plt.yticks(rotation=90)


plt.savefig('figure/green_space_index.pdf')

#################################################################
#this gives a hist of green space index: the result is not very good!
# m = load_variable('Data/distance_matrix.txt')
# c = m['Torrens Island']
# green_space = load_variable('Data/green_space_ultimate.txt')
# b = green_space[green_space['ogc_fid']==451]
# cc = b.geometry.iloc[0]

# plt.hist(np.array(cc), bins=160, color='blue', edgecolor='black')
