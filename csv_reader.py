# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:10:22 2020

@author: Titi
"""

import numpy as np
data = np.genfromtxt('data.csv', delimiter = ',')


def sample_select(first_line, lenght, input_lenght=8, output_length=1):
    global data
    input_matrix=data[first_line:first_line+lenght,0:input_lenght]
    output_matrix=data[first_line:first_line+lenght,input_lenght:input_lenght+output_length]
    #print(input_matrix)
    #print(output_matrix)
    return(input_matrix,output_matrix)
