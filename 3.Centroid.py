# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:11:10 2023

@author: Jiaqi Yao, Jingyu Duan

This file is used to find the centroid of all SA2s and store them as attributes of community
"""

#packages
import networkx as nx
import osmnx as ox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopy
from data_saver import save_variable, load_variable



##community data
community = load_variable('Data/community.txt')

#create a new list
centroids = []

#find geometry centroid
for i in range(len(community)):
    polygon = community.iloc[i,:]['geometry']
    centroid = polygon.centroid
    centroids.append(centroid)


##Add centroids to the dataframe
community['centroid'] = centroids

#Save data
save_variable(community,'Data/community_centroid.txt')
