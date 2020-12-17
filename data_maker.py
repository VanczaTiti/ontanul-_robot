# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:30:38 2020

@author: Titi
"""

import csv
import random
import dobas as dobas

dw_min=-0.500 #min szöggyorsulás
dw_max=10 # max szöggyorsulás
gene_lenght=8 #enyi elemből fog állni egy gén

line=0 #megírt adatsorok számlálása

#file megnyitás írásra
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    while line <1010000: #10^6 adat a tanításhoz 10^5 az ellenőrzéshez
        #véletlen szű egyed generálása
        tmp = [None] * (gene_lenght+1)
        for i in range(gene_lenght):
            tmp[i+1] = random.randrange(int(dw_min*100), int(dw_max*100))/100
        tmp[0]=0
        #Ha a dobás sikeres és páratlan sor következik
        if(dobas.dobasTav(tmp)<1 and line%2==0):
            writer.writerow([tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],1])
            line+=1
        #Ha a dobás sikertelen és páros sor következik
        if(dobas.dobasTav(tmp)==1 and line%2==1):
            writer.writerow([tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],0])
            line+=1
        #Ha egyik feltétel sem teljesült új egyedet generálunk
        
    