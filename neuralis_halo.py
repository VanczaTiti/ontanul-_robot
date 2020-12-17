# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 10:43:11 2020

@author: Titi
"""
import numpy as np
import csv_reader #Adatsor beolvasásához
np.set_printoptions(suppress=True) 

#aktivációs függvény:
def sigmoid(x):
    return 1/(1+np.exp(-x))

#Egy adott súlyok és torzítások esetén a hiba
def error(W1, W2, W3, W4, B1, B2, B3, B4): #W-k a súlymátrixok, B-k a torzításvektorok
    x1=np.dot(inputs, W1) + np.dot(np.ones((SEMP_SIZE,1)),B1)
    y1=sigmoid(x1)
    x2=np.dot(y1, W2) + np.dot(np.ones((SEMP_SIZE,1)),B2)
    y2=sigmoid(x2)
    x3=np.dot(y2, W3) + np.dot(np.ones((SEMP_SIZE,1)),B3)
    y3=sigmoid(x3)
    x4=np.dot(y3, W4) + np.dot(np.ones((SEMP_SIZE,1)),B4)
    output=sigmoid(x4)
    return(np.linalg.norm(target_output-output)**2/SEMP_SIZE)
    
#gradiens számítása numerikusan
def grad(E): #E a jelenlegi error
    grad_W1=np.zeros((DIM_in, DIM_l1))
    for i in range(DIM_in):
        for j in range(DIM_l1):
            d=np.zeros((DIM_in, DIM_l1))
            d[i,j]=0.00001
            grad_W1[i,j]=1/0.00001*(E-error(W1+d, W2, W3, W4, B1, B2, B3, B4))
    
    grad_W2=np.zeros((DIM_l1, DIM_l2))
    for i in range(DIM_l1):
        for j in range(DIM_l2):
            d=np.zeros((DIM_l1, DIM_l2))
            d[i,j]=0.00001
            grad_W2[i,j]=1/0.00001*(E-error(W1, W2+d, W3, W4, B1, B2, B3, B4))
            
    grad_W3=np.zeros((DIM_l2, DIM_l3))
    for i in range(DIM_l2):
        for j in range(DIM_l3):
            d=np.zeros((DIM_l2, DIM_l3))
            d[i,j]=0.00001
            grad_W3[i,j]=1/0.00001*(E-error(W1, W2, W3+d, W4, B1, B2, B3, B4))
    
    grad_W4=np.zeros((DIM_l3, DIM_out))
    for i in range(DIM_l3):
        for j in range(DIM_out):
            d=np.zeros((DIM_l3, DIM_out))
            d[i,j]=0.00001
            grad_W4[i,j]=1/0.00001*(E-error(W1, W2, W3, W4+d, B1, B2, B3, B4))
            
    grad_B1=np.zeros((1, DIM_l1))
    for i in range(DIM_l1):
        d=np.zeros((1, DIM_l1))
        d[0,i]=0.00001
        grad_B1[0,i]=1/0.00001*(E-error(W1, W2, W3, W4, B1+d, B2, B3, B4))
    
    grad_B2=np.zeros((1, DIM_l2))
    for i in range(DIM_l2):
        d=np.zeros((1, DIM_l2))
        d[0,i]=0.00001
        grad_B2[0,i]=1/0.00001*(E-error(W1, W2, W3, W4, B1, B2+d, B3, B4))
            
    grad_B3=np.zeros((1, DIM_l3))
    for i in range(DIM_l3):
        d=np.zeros((1, DIM_l3))
        d[0,i]=0.00001
        grad_B3[0,i]=1/0.00001*(E-error(W1, W2, W3, W4, B1, B2, B3+d, B4))
            
    grad_B4=np.zeros((1, DIM_out))
    for i in range(DIM_out):
        d=np.zeros((1, DIM_out))
        d[0,i]=0.00001
        grad_B4[0,i]=1/0.00001*(E-error(W1, W2, W3, W4, B1, B2, B3, B4+d))
        
    return(grad_W1,grad_W2,grad_W3,grad_W4,grad_B1,grad_B2,grad_B3,grad_B4)

#a háló tanításának elemi lépése az epoch    
def epoch(lr): #lr a változtatás ebességét határozza meg
    global W1, W2, W3, W4,  B1, B2, B3, B4
    E=error(W1, W2, W3, W4,  B1, B2, B3, B4)
    grad_W1,grad_W2,grad_W3,grad_W4,grad_B1,grad_B2,grad_B3,grad_B4=grad(E)
    W1+=grad_W1*lr
    W2+=grad_W2*lr
    W3+=grad_W3*lr
    W4+=grad_W4*lr
    B1+=grad_B1*lr
    B2+=grad_B2*lr
    B3+=grad_B3*lr
    B4+=grad_B4*lr
    
#tanítási ciklus
def learn(epochs=1, run_times=10, lr=1): 
    #epochs: egy semple-t hányszor vizsgáljon meg mielőtt a következőre lép
    #run_times: az adatsoron hányszor fusson végig
    #lr: a súlyok és torzítások változtatásának sebessége
    global inputs, target_output
    n=int(DATA_SIZE/SEMP_SIZE)
    for i in range(run_times):
        (inputs,target_output)= csv_reader.sample_select(DATA_SIZE,SEMP_SIZE)
        #aktuális adatok kiiratása, jól jön a hosszú futásidő miatt
        print("lr=", lr ,"run ", i, "error: ", error(W1, W2, W3, W4, B1, B2, B3, B4))
        for j in range(n):
            (inputs,target_output)= csv_reader.sample_select(j*SEMP_SIZE,SEMP_SIZE)
            for e in range(epochs):
                epoch(lr)

#rétegek dimenziói
DIM_in=8
DIM_out=1
DIM_l1=20
DIM_l2=20
DIM_l3=10
SEMP_SIZE=1000
DATA_SIZE=400000

#súlymátrixok, és torzítás vektorok incializálása
W1=np.random.rand(DIM_in, DIM_l1)-0.5
B1=np.zeros((1, DIM_l1))
W2=np.random.rand(DIM_l1, DIM_l2)-0.5
B2=np.zeros((1, DIM_l2))
W3=np.random.rand(DIM_l2, DIM_l3)-0.5
B3=np.zeros((1, DIM_l3))
W4=np.random.rand(DIM_l3, DIM_out)-0.5
B4=np.zeros((1, DIM_out))


#Háló tanítása, csökkenő lr értékkel
learn(1, 10, 5)
learn(1, 10, 1.5)
learn(1, 10, 0.5)
learn(1, 10, 0.15)
learn(1, 10, 0.05)

#ellenőrzás a háló által nem látott adatsoron
print("ellenőrzés")
#100 elem kiiratása
SEMP_SIZE=100
(inputs,target_output)= csv_reader.sample_select(DATA_SIZE,SEMP_SIZE)
x1=np.dot(inputs, W1) + np.dot(np.ones((SEMP_SIZE,1)),B1)
y1=sigmoid(x1)
x2=np.dot(y1, W2) + np.dot(np.ones((SEMP_SIZE,1)),B2)
y2=sigmoid(x2)
x3=np.dot(y2, W3) + np.dot(np.ones((SEMP_SIZE,1)),B3)
y3=sigmoid(x3)
x4=np.dot(y3, W4) + np.dot(np.ones((SEMP_SIZE,1)),B4)
output=sigmoid(x4)
hibak=0
err=output-target_output
for i in range(SEMP_SIZE):
    if (abs(err[i])>0.5):
        hibak+=1
print(np.dot(output,[[1,0, -1]])+np.dot(target_output,[[0,1,1]]))
print("network    target     error ")
print(hibak, " misses")

#10000 elem vizsgálatával a hibázási százalék közelítése
SEMP_SIZE=10000
(inputs,target_output)= csv_reader.sample_select(DATA_SIZE,SEMP_SIZE)
x1=np.dot(inputs, W1) + np.dot(np.ones((SEMP_SIZE,1)),B1)
y1=sigmoid(x1)
x2=np.dot(y1, W2) + np.dot(np.ones((SEMP_SIZE,1)),B2)
y2=sigmoid(x2)
x3=np.dot(y2, W3) + np.dot(np.ones((SEMP_SIZE,1)),B3)
y3=sigmoid(x3)
x4=np.dot(y3, W4) + np.dot(np.ones((SEMP_SIZE,1)),B4)
output=sigmoid(x4)
hibak=0
err=output-target_output
for i in range(SEMP_SIZE):
    if (abs(err[i])>0.5):
        hibak+=1
print(hibak/SEMP_SIZE*100, "%")

#súlyok és torzítások elmentése .csv filokba
np.savetxt("W1.csv", W1, delimiter=",")
np.savetxt("W2.csv", W2, delimiter=",")
np.savetxt("W3.csv", W3, delimiter=",")
np.savetxt("W4.csv", W4, delimiter=",")
np.savetxt("B1.csv", B1, delimiter=",")
np.savetxt("B2.csv", B2, delimiter=",")
np.savetxt("B3.csv", B3, delimiter=",")
np.savetxt("B4.csv", B4, delimiter=",")
