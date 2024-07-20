# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 17:50:48 2024

@author: Jiaqi Yao, Jingyu Duan

This file try to load, preprocess, plot and store data on green space
"""


#Packages
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

# Shapefile path
shapefile_path = "Data/SA_POS/SA_POS.shp"
community = load_variable('Data/community_centroid.txt') 

# load Shapefile using geopandas
gdf = gpd.read_file(shapefile_path)
gdf_latlon = gdf.to_crs(epsg=4326) #coordinate conversion


############################################################################
#plot green space


plt.style.use('seaborn-whitegrid')


column_to_plot = 'type'
cmap = 'viridis'


ax = gdf_latlon.plot(color = 'green',figsize=(6,6), alpha=0.5)
ctx.add_basemap(ax, crs=gdf_latlon.crs.to_string(),source=ctx.providers.OpenStreetMap.France) #add base map to our figure


plt.xlabel('Longitude', fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
plt.ylabel('Latitude',  fontsize=16, fontdict={'fontname': 'Times New Roman', 'fontsize': 16})

# plt.xticks(rotation=90)
# plt.yticks(rotation=90)

plt.savefig('figure/green_space_distribution.pdf')


plt.show()


###############################
#save data
save_variable(gdf_latlon,'Data/green_space.txt')