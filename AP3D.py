from math import sqrt, floor
import numpy as np
import time
import pandas as pd
import random

def dados (seed,ncasos):
    a1=[]
    c1=[]
    a2=[]
    c2=[]
    a3=[]
    c3=[]
    a4=[]
    c4=[]
    a5=[]
    c5=[]
    random.seed(seed)
    for i in range (0,ncasos):
        condiçao1=1
        condiçao2=1
        condiçao3=1
        condiçao4=1
        ai = random.randint(1, 1000)
        ci = random.randint(1, 1000)
        a1.append(ai)
        c1.append(ci)
        while condiçao1==1:
            aii = random.randint(1, 1000)
            cii = random.randint(1, 1000)

            if ai>=aii and ci<=cii:
                a2.append(aii)
                c2.append(cii)
                condiçao1=0
        while condiçao2==1:
            aiii = random.randint(1, 1000)
            ciii = random.randint(1, 1000)

            if aii>=aiii and cii<=ciii:
                a3.append(aiii)
                c3.append(ciii)
                condiçao2=0

        while condiçao3==1:
            aiiii = random.randint(1, 1000)
            ciiii = random.randint(1, 1000)

            if aiii>=aiiii and ciii<=ciiii:
                a4.append(aiiii)
                c4.append(ciiii)
                condiçao3=0
    
        while condiçao4==1:
            aiiiii = random.randint(1, 1000)
            ciiiii = random.randint(1, 1000)

            if aiiii>=aiiiii and ciiii<=ciiiii:
                a5.append(aiiiii)
                c5.append(ciiiii)
                condiçao4=0
    return [a1,c1,a2,c2,a3,c3,a4,c4,a5,c5]

def AP3D(a,c):
    kmax=0
    npontos=0
    
    for i3 in range (floor(a[2])+1):
                raiz1= max(0.0,1-(i3**2/a[2]**2))
                a_1=a[0]*sqrt(raiz1)
                a_2=a[1]*sqrt(raiz1)

                for i1 in range(floor(a_1)+1):
                    npontos=npontos+1
                    if a_1!=0:
                        i2=floor(a_2 * sqrt(1 - (i1**2 / a_1**2)))
                    else:
                        i2=0
                    pt=np.array([i1,i2,i3])
                    if pt@c>kmax:
                        pmaior=pt
                        kmax=pt@c
    return [pmaior,kmax,npontos]

columns=['A1','A2','A3','C1','C2','C3','Tempo','K max','Ponto','Dentro Elips','Nº pontos analisados']
ncasos=1000
seed=74
pont=[]
res=[]
tim=[]
dentro=[]
totalpontos=[]

(ai,ci,aii,cii,aiii,ciii,aiiii,ciiii,aiiiii,ciiiii)=dados(seed,ncasos)

for j in range (ncasos):
    print(j)
    a=np.array([ai[j], aii[j], aiii[j]])
    c=np.array([ci[j], cii[j], ciii[j]])
    init = time.perf_counter()
    (ponto,k,qtdpontos)=AP3D(a,c)
    endt = time.perf_counter()
    tim.append((endt-init))
    res.append(k)
    pont.append(ponto)
    totalpontos.append(qtdpontos)
    if ( (ponto[2]**2 / a[2]**2)+ (ponto[1]**2 / a[1]**2)+ (ponto[0]**2 / a[0]**2))<=1:
      dentro.append(1)
    else:
      dentro.append(0)

    df = pd.DataFrame(list(zip(ai,aii,aiii,ci,cii,ciii,tim,res,pont,dentro,totalpontos)), columns=columns)
    df.to_excel(r"C:\Users\lucas_mzj9txp\Desktop\AP3D.xlsx")