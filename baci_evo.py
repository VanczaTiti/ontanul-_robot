# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 12:57:39 2020

Bakteriális algoritmus

@author: Titi
"""
import random
import numpy as np
import dobas 
import halo 

np.set_printoptions(suppress=True)

dw_min=-0.500 #min szöggyorsulás
dw_max=10 # max szöggyorsulás
gene_lenght=8 #enyi elemből fog állni egy gén
pop_size=16 #párosnak kell lennie
N_clone=1 # bacteriális mutáció közben hány másolatot készít
N_inf=20#generációnkénti infekciók számát jelóli
N_change=2 #ennyi egyed megy akukába generációnként, és helyére egy új jön
Sigma_fix=0.35 #random gauss eloszláshoz minden esetben
Sigma_prop=5.5 #random gauss eloszláshoz: Sigma_prop/fittness


def rand_individual(): #generál egy rendom egyedet melynek hossza gen_lenght+1, és az elejére helyez egy 0 értéket, melybe később az egyed fitnese kerül
    individual = [None] * (gene_lenght+1)
    for i in range(gene_lenght):
        individual[i+1] = random.randrange(int(dw_min*100), int(dw_max*100))/100
    individual[0]=0
    return(individual)

def new_individual():#generál egy egyedet aki képes eldobni a labdát, ehhez tesztel.
    for i in range(1000): #ha ezernél töbször fut álljon le
        individual =rand_individual()
        if (halo.test(individual)>0.6): #ha a neurális háló szerint a dobás sikeres az érték1-hez közeli
            if(dobas.dobasTav(individual)<1):#ha az eldobás sikrtelen a dobas tav fv 1-et [m] ad vissza (a cél negatív irányban van)
                individual[0]=round(100/(dobas.hibafv(individual)+0.000001),2)
                dobas.cnt-=1 #dobas tav és fiba fv is növeli a counter értékét, meg lehetne oldani hogy csak az egyiket kelljen meghívni ezért levonok egyet
                return(individual)
    print('new individual túcsordult')
    return(np.zeros(gene_lenght+1))
            
def gen_0(): #egy mátrikba teszi az új egyedeket, mindegyik el tudja dobni a labdát (első oszlop már nem 0)
    pop=np.zeros(shape=(pop_size,  gene_lenght+1))
    for i in range(pop_size):
        pop[i,]=new_individual()
    return(pop)
    
def mut_cromosome(copies, i): # copies:mátrix, i:hányadik elemet mutálja
    #utolsó sor kivételével véletlenszerűen mutálja az másolatok kiválasztott elemét
    for j in range(N_clone):
        copies[j,i]+=round(float(np.random.normal(0, Sigma_fix+Sigma_prop/copies[N_clone,0], 1)), 2)
        copies[j,0]=0#ha az első elemet lenullázom akkor így átadhatom a hiba függvénynek
        copies[j,0]=round(100/(dobas.hibafv(copies[j,])+0.000001),2)
        if (copies[j,0]>=copies[N_clone,0]): #ha "jobb" lett egy másolat az eredetinél akkor behelyettesítem
            copies[N_clone,]=copies[j,]
    for i in range(N_clone):#minden másolatot a legjobb egyedre cserélek
        copies[i,]=copies[N_clone,] 
    #nem kell return, mert magát a mátrixot módosítja
            
def bact_mutation(ind):#1 egyeden végez bakteriális mutációt, visszatér az eredménnyel
    copies=np.zeros(shape=(N_clone+1,  gene_lenght+1))
    for i in range(N_clone+1):
        copies[i,]=ind
    for i in range(gene_lenght):
        mut_cromosome(copies, gene_lenght-i)
    return(copies[0,])
    
def mutate_pop(pop):#egész populáción végez bacteriális mutációt
    for i in range(pop_size):
        pop[i,]=bact_mutation(pop[i,])
        
def infect(target, source):#A sours egyik elemét átmásolja a tergetba, visszatér a pontosabb egyeddel
    tmp = target.copy()
    i=random.randrange(1, gene_lenght)
    tmp[i]=source[i]
    tmp[0]=0
    tmp[0]=round(100/(dobas.hibafv(tmp)+0.000001),2)
    if(tmp[0]>target[0]):
        return (tmp)
    else:
        return(target)
        
def bouble_sort(pop):#bouble rendezést végez a populáción, 0. sorban lesz a legpontosabb
    tmp = [None] * (gene_lenght+1)
    for i in range(pop_size-1):
        for j in range( pop_size-i-1):
            if(pop[j,0]<pop[j+1,0]):
                tmp=pop[j,].copy()
                pop[j,]=pop[j+1,].copy()
                pop[j+1,]=tmp.copy()
            
def infect_pop(pop): #a populáción N_inf számú infekciót hajt végre
    bouble_sort(pop)
    for i in range(N_inf):
        s=random.randrange(0, pop_size/2)#A source a pontosabb felének egyik eleme
        t=random.randrange(0, pop_size/2)+int(pop_size/2)#A target a pontatlanabb felének egyik eleme
        pop[t,]=infect(pop[t,], pop[s,])
        
def change(pop): #a populáció N_inf leg pontatlanabb egyede helyett új egyedeket hoz létre
    bouble_sort(pop)
    for i in range(N_change):
        pop[-i,]=new_individual()


'''innentől számolás'''
'''meg szeretnénk tudni, hogy az adott beállításokkal hány dobás kell ahhoz, hogy legyen 10 pontos egyed'''
run_times=5 #hány futtatás eredményét szeretnénk átlagolni

dobas.cnt=0 #minden dobásnál egyel nő 
for r in range(run_times):
   # if(r%100==0):
        #print(r)
    population=gen_0()
    bouble_sort(population)
    while(population[9,0]<10000): #amíg  10. legjobb dobás hibály több mint 0,1 cm
        change(population)
        mutate_pop(population)
        infect_pop(population)
        bouble_sort(population)
    
    
print('run times: ', run_times)
print('gene_lenght: ', gene_lenght, ' pop_size: ', pop_size, ' N_clone: ', N_clone, ' N_inf: ', N_inf, ' Sigma_fix: ', Sigma_fix, ' Sigma_prop: ', Sigma_prop)
print('becterial: ',dobas.cnt/run_times)


