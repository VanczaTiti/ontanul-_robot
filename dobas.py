# -*- coding: utf-8 -*-
"""
Egy egyszerű szimulációja a robotnak.

@author: Titi
"""
import math

l= 0.05 # a kar hossza (a forgás középpont és a golyó tömegközéppontjának távolsága) [m]
A=80 # a kar végének szöge: 0-> egyenes ród 90-> golyóval érintkező egyik lap merőleges a sugárra
fi_0 = 0*math.pi/6  #a kar kezdeti szögelfordulása [rad], 0=lefelé
g=-10 #gravitáció
sin=0.05 #lap dőlésszögének sinusa
a=g*sin #golyó gyorsulása y irányba
cel=-20/100 #cél távolság megadása [m]
dt=0.1    #időlépés

dw=[0] #a kar szöggyorsulása [rad/s^2]
cnt=0 #elvégzett dobások száma


def dobas(w): #egy szögsebesség görbébéől megadja, hogy a golyó honnan [m], milyen sebességgel [m/s] repül el
    global cnt
    cnt+=1
    fi=[fi_0] #a kar szögelfordulása [rad], 0=lefelé
    dw=[0] #a kar szöggyorsulása [rad/s^2]
    w_pr=0
    for w_tmp in w:
        fi.append(fi[-1]+w_tmp*dt)
        dw.append((w_tmp-w_pr)/dt)
        a_cp=w_pr*w_pr*l #centripetális gyorsulás számítása
        a_t=dw[-1]*l #tangenciális gyorsulás számítása
        #print("sor", a_cp, a_t, math.tan(A/180*math.pi))
        if a_cp>a_t*math.tan(A/180*math.pi):
            #print("a golyó elrepült")
            x_0=math.sin(fi[-2])*l
            y_0=(-math.cos(fi[-2]))*l
            v_x0=l*w_pr*math.cos(fi[-2])
            v_y0=l*w_pr*math.sin(fi[-2])
            #print("w:", w_pr, "\n r_0 [mm]:", x_0*1000, y_0*1000, "\n v_0 [mm/s]:", v_x0*1000, v_y0*1000)
            return([x_0, y_0], [v_x0, v_y0])
        w_pr=w_tmp
    #print("a golyó nem repült el a vizsgált idő alatt")
    return([0, 0], [0, 0])
    
def dobasTav(dw): #A sebbesség görbéből visszaadja a visszaeső golyó x koordinátáját [m] ahol y=0
    #ha a golyót nem sikerűl eldobni +1-el tér vissza.
    w=[0]
    for dw_tmp in dw:
        w.append(w[-1]+dw_tmp*dt)
    r_0, v_0=dobas(w)
    if r_0==[0,0] or v_0[1]<=0 or v_0[1]*v_0[1]<=2*r_0[1]*a:
        return(+1)
    else:
        t1=(-v_0[1]+math.sqrt(v_0[1]**2-2*a*r_0[1]))/a
        t2=(-v_0[1]-math.sqrt(v_0[1]**2-2*a*r_0[1]))/a
        if t1>t2:
            t=t1
        else:
            t=t2                
        #print(t)
        return(r_0[0]+t*v_0[0])        
        
def hibafv(dw): #a sebességgörbéből, visszatér a céltól cm-ben számított hiba négyzetével
    return(((cel-dobasTav(dw))*100)**2)

