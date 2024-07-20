# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 11:31:19 2024

@author: Jiaqi Yao, Jingyu Duan

This file try to load, preprocess, plot and store data about median income of each SA2 region
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

#load data
community = load_variable('Data/community_income.txt')
green_space = load_variable('Data/green_space.txt')

population = gpd.read_file('Data/ERP_SA2/SA2 ERP GeoPackage 2022.gpkg') #SA2 population data 

#LGA is a larger zoning, more information can be found on the ABS official website
LGA = gpd.read_file('Data/ERP_LGA/LGA ERP GeoPackage 2022.gpkg') #LGA population data

####################################################################
#Find population data in SA
population_ade = population[population['State_name_2021']=='South Australia']
LGA_ade = LGA[LGA['State_name_2021']=='South Australia']


##################################################################
#congestion


den = np.zeros((len(green_space),1)) #create empty list

#If green space intersects with one or more than one SA2s, assign its congestion as the largest congestion of SA2s 
for i in range(len(green_space)):
    green = green_space.iloc[i,:]['geometry']
    den1 = 0.0
    
    for j in range(len(population_ade)):

        people = population_ade.iloc[j,:]['geometry']
        
        if people.intersects(green):
            
            den2 = population_ade.iloc[j,:]['Pop_density_2022_people_per_km2']
            if (den2>den1):
                den1 = den2
    
    den[i,0] = den1


#Some green space doe not belong to any SA2, assign its congestion as the one of the nearest SA2 
for i in range(len(den)):
    if (den[i][0]==0.0):
        poly1 = green_space.iloc[i,:]['geometry']
        
        poly_selected = 9999999
        dist = np.inf
        
        for j in range(len(population_ade)):
            poly2 = population_ade.iloc[j,:]['geometry']
            
            dist1 = poly1.distance(poly2)
            if (dist1<dist):
                poly_selected = j
                dist = dist1
        
        if (poly_selected != 9999999):
           den[i,0] = population_ade.iloc[poly_selected,:]['Pop_density_2022_people_per_km2']


#Some of the SA2 has 0 congestion, which means the congestion of some green space is 0.
#For that kind of green space, substitue its congestion as the one of the LGA it belongs to.
for i in range(len(den)):
    if(den[i][0] == 0.0):
        poly1 = green_space.iloc[i,:]['geometry']
        den1 = 0.0
        
        for j in range(len(LGA_ade)):

            people = LGA_ade.iloc[j,:]['geometry']
            
            if people.intersects(green):
                
                den2 = LGA_ade.iloc[j,:]['Pop_density_2022_people_per_km2']
                if (den2>den1):
                    den1 = den2
        
        den[i,0] = den1


# Save variable
green_space['density'] = den
save_variable(den, 'Data/density.txt')
save_variable(green_space, 'Data/green_space222.txt')
#############################################################################################################
#Area 

#calculate area
green_area = []

# specify a named ellipsoid
geod = Geod(ellps="WGS84")

#Find area
for i in range(len(green_space)):
    poly = green_space.iloc[i,:]['geometry']
    area = abs(geod.geometry_area_perimeter(poly)[0])
    
    green_area.append(area/1000000) #km^2 as unit
    
#save data
green_space['area'] = green_area
save_variable(green_space, 'Data/green_space_ultimate.txt')

