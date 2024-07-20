# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:20:46 2024

@author: Jiaqi Yao, Jingyu Duan

This file gives a scatter of our result
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
from scipy.stats import linregress


'''
Notice: Here we plot median vs log(green index)
'''

#data
median = pd.read_csv('Data/Adelaide_income.csv',header=0)
gdf = load_variable('Data/community_ultimate.txt')

x = list(median['Median'])
y = list(gdf['log_index'])

slope, intercept, r_value, p_value, std_err = linregress(x,y)


###############################################3
#style
plt.style.use('ggplot')

# plot
plt.scatter(x, y, color='blue', marker='o', label='SA2 Community')


#plt.title('Median Income VS Log Green Space Index by Statistical Area 2')
plt.xlabel('Median Income', fontdict={'fontname': 'Times New Roman', 'fontsize': 16})
plt.ylabel('Log Green space index', fontdict={'fontname': 'Times New Roman', 'fontsize': 16})


plt.legend(prop={"family" : "Times New Roman",'size':14},loc='best', edgecolor='black')



plt.savefig('figure/scatter_plot_log.pdf')


