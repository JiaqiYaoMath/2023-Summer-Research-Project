# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 23:05:13 2024

@author: Jiaqi Yao, Jingyu Duan

This file try to load, preprocess, plot and store data about median income of each SA2 region
"""

#Package
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

#community data
community = load_variable('Data/community_centroid.txt')

#Median data
income = pd.read_csv('Data/income_Adelaide.csv', header= 0 )
median = list(income['Median'])

#Store and save data
community['Median'] = median
save_variable(community, 'Data/community_income.txt')