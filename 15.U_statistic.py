# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 16:55:33 2023

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
from scipy.stats import mannwhitneyu

community = load_variable('Data/community_ultimate.txt')
mean_low = np.mean(community['Median'])



high_low = []
low_low = []

for i in range(len(community)):
    data = community.iloc[i,:]
    
    if (data['Median']<mean_low):
        low_low.append(data['green_index'])
    else:
        high_low.append(data['green_index'])
        
        
# 执行 Mann-Whitney U 检验
statistic, p_value = mannwhitneyu(  high_low, low_low)

# 输出检验统计量和 p-value
print("Mann-Whitney U test statistic:", statistic)
print("p-value:", p_value)