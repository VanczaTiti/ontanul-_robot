"""
Created on Fri Oct  2 12:57:39 2020

@author: Titi
"""
import random
import numpy as np
import dobas 
dw_min=-0.5001 #min szöggyorsulás
dw_max=10 # max szöggyorsulás
gene_lenght=11 #enyi elemből fog állni egy gén
rand=0 #generációként enyi új random egyed lesz
mut=5 #generációként ennyi mutálódott egyed lesz
stay=5#ennyi egyed fog megmaradni az előző generációból
cross=3 #generációnként 2* ennyi crossoverrel lértejött egyed lesz
sigma=1.4 #random gauss eloszláshoz

pop_size=rand+mut+cross*2+stay


def rand_individual(): #generál egy rendom egyedet melynek hossza gen_lenght+1, és az elejére helyez egy 0 értéket, melybe később az egyed fitnese kerül
    individual = [None] * (gene_lenght+1)
    for i in range(gene_lenght):
        individual[i+1] = random.randrange(int(dw_min*100), int(dw_max*100))/100
    individual[0]=0
    return(individual)
    
def gen_0():# nulladik generációt adja vissza egy mátroxba, első oszlop 0, egyedek soronként
    pop=np.zeros(shape=(pop_size-stay,  gene_lenght+1))
    for i in range(pop_size-stay):
        ind=rand_individual()
        for j in range (gene_lenght+1):
            pop[i,j]=ind[j]
    return(pop)
    
def pop_fitness(pop):#minden egyed fitneszét beírja az első oszlopba
    for i in range(pop_size-stay):
        dw=pop[i,1:gene_lenght]
        pop[i,0]=round(100/(dobas.hibafv(dw)+0.000001),2)
        
def select(pop):#fitnesszével arányos eséllyel adja vissza az populáció egyik egyedét
    tmp=0
    s=np.sum(pop[:,0])
    r=random.uniform(0,s)
    for i in range(pop_size):
        tmp+=pop[i,0]
        if tmp>=r:
            return(pop[i,:])
    

def crossover(pop):#két egyedet választ ki, és genetikáját keveri. Egy 2*N-es mátrixba adja őket vissza
    inv1=select(pop)
    inv2=select(pop)
    r=random.randrange(gene_lenght)+1
    inv_tmp=inv1
    inv1=np.append(inv1[0:r],inv2[r:gene_lenght+1])
    inv2=np.append(inv2[0:r],inv_tmp[r:gene_lenght+1])
    inv1[0]=0;
    inv2[0]=0;
    return(np.vstack((inv1,inv2)))

def mutation(pop):#egy egyedet választ ki, és mutál
    inv=select(pop)
    inv_mut = [None] * (gene_lenght+1)
    for i in range(gene_lenght):
        inv_mut[i+1] = round(inv[i+1]+float(np.random.normal(0, sigma, 1)), 2)
    inv_mut[0]=0
    inv[0]=0
    return(inv_mut)

def next_gen(pop):#1 generáció
    next_gen=np.zeros(shape=(pop_size,  gene_lenght+1))
    for i in range(rand):#rand számú új egyed lesz
        ind=rand_individual()
        for j in range (gene_lenght+1):
            next_gen[i,j]=ind[j]
    for i in range(cross):#2*cross számú kersztezett egyed
        ind_pair=crossover(pop)
        for j in range (gene_lenght+1):
            next_gen[rand+2*i,j]=ind_pair[0,j]
            next_gen[rand+2*i+1,j]=ind_pair[1,j]
    for i in range(mut):#mut számú mutálódott
        ind_pair=mutation(pop)
        for j in range (gene_lenght+1):
            next_gen[rand+2*cross+i,j]=ind_pair[j]
    for i in range(stay):#mut számú mutálódott
        ind_pair=select(pop)
        for j in range (gene_lenght+1):
            next_gen[rand+2*cross+mut+i,j]=ind_pair[j]
    return(next_gen)
    

'''innentől számolás'''
'''meg szeretném tudni, hogy az adott beállításokkal hány dobás kell ahhoz, hogy legyen 10 pontos egyed'''

run_times=10 #ennyi futás átlagát számolja ki
dobas.cnt=0
for r in range(run_times):
    hit=0
    polulaton=gen_0()
    while(hit<10):
        pop_fitness(polulaton)
        hit=0
        for j in range(np.shape(polulaton)[0]):
            if(polulaton[j,0]>10000):#ez 0,1 cm-nél kisebb hibát jelent
                hit+=1       
        #print(r,". gen, hit:",hit)
        polulaton=next_gen(polulaton)
    
print('run times: ', run_times)
print('rand: ', rand, ' mut: ', mut, ' stay: ', stay, ' cross: ', cross, ' sigma: ', sigma)
print('genetic:', dobas.cnt/run_times)