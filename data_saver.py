# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 10:50:09 2023

@author: 23783
"""

import pickle


def save_variable(v,filename):
    f=open(filename,'wb')
    pickle.dump(v,f)
    f.close()
    return filename
 
def load_variable(filename):
   f=open(filename,'rb')
   r=pickle.load(f)
   f.close()
   return r
