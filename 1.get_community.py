"""
Created on Wed Nov 29 22:09:17 2023

@author: Jiaqi Yao, Jingyu Duan

This file is used to collect and store data on SA2
"""

# Load Packages
import geopandas as gpd
from shapely.geometry import Polygon, Point
from data_saver import save_variable, load_variable
import pandas as pd


# Shapefile path
shapefile_path = "Data/SA2_2021_AUST_SHP_GDA2020/SA2_2021_AUST_GDA2020.shp"

# load Shapefile using geopandas
gdf = gpd.read_file(shapefile_path)


#select SA2 region for Adelaide
adelaide_data = gdf[gdf['GCC_NAME21']=='Greater Adelaide']


# Add some more SA2s
Mallala = gdf[gdf['SA2_NAME21']=='Mallala']
Lyndoch = gdf[gdf['SA2_NAME21']=='Lyndoch']
Tanunda = gdf[gdf['SA2_NAME21']=='Tanunda']
Nuriootpa = gdf[gdf['SA2_NAME21']=='Nuriootpa']
Barossa_Angaston = gdf[gdf['SA2_NAME21']=='Barossa - Angaston']
Strathalbyn = gdf[gdf['SA2_NAME21']=='Strathalbyn']
Strathalbyn_Surrounds = gdf[gdf['SA2_NAME21']=='Strathalbyn Surrounds']
Yankalilla = gdf[gdf['SA2_NAME21']=='Yankalilla']
Victor_Harbor = gdf[gdf['SA2_NAME21']=='Victor Harbor']
Goolwa_PortElliot = gdf[gdf['SA2_NAME21']=='Goolwa - Port Elliot']

adelaide_data = pd.concat([adelaide_data, Mallala], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Lyndoch], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Tanunda], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Nuriootpa], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Barossa_Angaston], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Strathalbyn], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Strathalbyn_Surrounds], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Yankalilla], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Victor_Harbor], ignore_index=True)
adelaide_data = pd.concat([adelaide_data, Goolwa_PortElliot], ignore_index=True)

########################
#save our data
save_variable(adelaide_data,'Data/community.txt')