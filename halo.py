# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:33:57 2020

@author: Titi
"""

import numpy as np
np.set_printoptions(suppress=True)

gene_lenght=8 #enyi elemből fog állni egy gén

#aktivációs függvény:
def sigmoid(x):
    return 1/(1+np.exp(-x))

#súlyok és torzítások kilvasása .csv filokból
W1 = np.genfromtxt("W1.csv", delimiter=',')
W2 = np.genfromtxt("W2.csv", delimiter=',')
W3 = np.genfromtxt("W3.csv", delimiter=',')
W4 = np.genfromtxt("W4.csv", delimiter=',')
B1 = np.genfromtxt("B1.csv", delimiter=',')
B2 = np.genfromtxt("B2.csv", delimiter=',')
B3 = np.genfromtxt("B3.csv", delimiter=',')
B4 = np.genfromtxt("B4.csv", delimiter=',')

#egy egyed vizsgálata a háló által
def test(input_vec):
    global W1, W2, W3, W4, B1, B2, B3, B4
    input_vec=input_vec[1:gene_lenght+1]
    x1=np.dot(input_vec, W1) + B1
    y1=sigmoid(x1)
    x2=np.dot(y1, W2) + B2
    y2=sigmoid(x2)
    x3=np.dot(y2, W3) + B3
    y3=sigmoid(x3)
    x4=np.dot(y3, W4) + B4
    output=sigmoid(x4)
    return(output)

