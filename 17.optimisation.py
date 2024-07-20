
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 14:28:06 2023

@author: 23783
"""

import numpy as np
import matplotlib.pyplot as plt
from data_saver import save_variable, load_variable
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from pyscipopt import Model,quicksum, multidict


community = load_variable('Data/community_income_green.txt')
adj_dataframe = load_variable('Data/adjacency_matrix.txt')
green_index = load_variable('Data/green_index.txt')


adj = np.matrix(adj_dataframe).astype(int)

def adjacency_matrix_to_weight_matrix(adjacency_matrix):
    
    num_nodes = len(adjacency_matrix)
    
    
    weight_matrix = np.zeros((num_nodes, num_nodes))
    
    # Iterate through each line
    for i in range(num_nodes):
        # Calculate the sum of the non-zero elements of the current row
        row_sum = adjacency_matrix[i,:].sum()
        
        # If the sum of the non-zero elements of the current row is zero, keep the current row of the weight matrix as zero
        if row_sum == 0:
            weight_matrix[i] = np.zeros(num_nodes)
        else:
            # Compute the current row of the neighbor weight matrix
            weight_matrix[i] = adjacency_matrix[i] / row_sum
    
    return weight_matrix

wei = adjacency_matrix_to_weight_matrix(adj)


##############################################################################
income = np.array(community['low_income'])
green = np.array(green_index)
# income_nor = -1 + 2/(max(income)-min(income))*(income-min(income))


# sns.histplot(income, kde=True)
# plt.title('Histogram with Kernel Density Estimate')
# plt.xlabel('Value')
# plt.ylabel('Density')
# plt.show()

##########################standlisation
data_array  = [[x] for x in income]
green_array = [[y] for y in green[:,0]]
scaler = StandardScaler()

# Means and standard deviations were calculated and standardized
scaled_data = scaler.fit_transform(data_array)
scaled_green = scaler.fit_transform(green_array)

# sns.histplot(scaled_data, kde=True)
# plt.title('Histogram with Kernel Density Estimate')
# plt.xlabel('Value')
# plt.ylabel('Density')
# plt.show()

income_nor1 = scaled_data/max(abs(scaled_data))
green_nor1 = scaled_green/max(abs(scaled_green))
income_nor = []
green_nor = []
for nor in income_nor1:
    income_nor.append(nor[0])
    
for nor2 in green_nor1:
    green_nor.append(nor2[0])
# sns.histplot(income_nor, kde=True)
# plt.title('Histogram with Kernel Density Estimate')
# plt.xlabel('Value')
# plt.ylabel('Density')
# plt.show()

sns.histplot(green_nor, kde=True)
plt.title('Histogram with Kernel Density Estimate')
plt.xlabel('Value')
plt.ylabel('Density')
plt.show()

save_variable(income_nor, 'Data/income_nor.txt')
save_variable(income_nor, 'Data/green_nor.txt')
####################################################################################
#Set model
model = Model("green space") 


#Set variable
x ={}

for i in range(len(income_nor)):
    x[i] = model.addVar(lb=-1,ub=1,vtype="C",name="x(%s)"%i)

sumy = {}

for i in range(len(income_nor)):
    sumy[i] = model.addVar(vtype="C",name="sumy(%s)"%i)

# var.name(model)
# all_vars = model.getVars()

n = len(income_nor)
#set objective
model.setObjective(
    quicksum(income_nor[i]*sumy[i] for i in range(n)),'maximize')

#set constraint
for i in range(len(income_nor)):
    model.addCons(sumy[i] == quicksum(wei[i][j]*x[j] for j in range(len(income_nor))))


model.optimize()
sol = model.getBestSol()

solution =[]
for i in range(n):
    solution.append(sol[x[i]])
    
solution_a = np.array(solution)
c = solution_a - green_nor