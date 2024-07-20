# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 15:49:29 2024

@author: Jiaqi Yao, Jingyu Duan

This file gives a visualisation of green space
"""

#package
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
import geopandas as gpd
from data_saver import save_variable, load_variable
from shapely.geometry import Polygon
from shapely.geometry import Point
import copy
import contextily as ctx
from pyproj import Proj, Transformer

#data
green_space = load_variable('Data/green_space_promax.txt')
green_space = gpd.GeoDataFrame(green_space)

#style
plt.style.use('seaborn-whitegrid')


column_to_plot = 'category'
cmap = 'viridis'

##########################################################################
# plot polygon
c = green_space.plot(figsize=(10, 6), alpha=0.5,column=column_to_plot, cmap=cmap, legend=True)
#ctx.add_basemap(c ,crs=green_space.crs.to_string(),source=ctx.providers.OpenStreetMap.France)


plt.xlabel('longitude', fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
plt.ylabel('Latitude', fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
plt.savefig('figure/green_space_distribution.pdf')

plt.show()
