from math import sqrt, floor, ceil
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

def relaxado (a1,a2,i3,i4,i5,c1,c2,c,kmax,pmaior,npontos):
    lambda_val = sqrt(c1**2 * a1**2 + c2**2 * a2**2)
    P = np.array([floor(c1 * a1**2 / lambda_val),floor(c2 * a2**2 / lambda_val)])


    b = c1*P[0] + c2*P[1]

    beta1 = (a1**2 * b * c1 + a1 * a2 * c2 * sqrt(a1**2 * c1**2 + a2**2 * c2**2 - b**2)) / (a2**2 * c2**2 + a1**2 * c1**2)
    beta2 = (a1**2 * b * c1 - a1 * a2 * c2 * sqrt(a1**2 * c1**2 + a2**2 * c2**2 - b**2)) / (a2**2 * c2**2 + a1**2 * c1**2)


    xd = np.array([beta1, (b - c1 * beta1) / c2])
    xe = np.array([beta2,(b-c1*beta2)/c2])

    for i1 in range (max(0,floor(xe[0])),min(floor(a1),(ceil(xd[0])))+1):
        npontos=npontos+1

        i2=floor(a2 * sqrt(1 - (i1**2 / a1**2)))

        pt=np.array([i1,i2,i3,i4,i5])
        if pt@c>kmax:
            pmaior=pt
            kmax=pt@c

    return(kmax,pmaior,npontos)

def AL5D(a,c):
    kmax=0
    npontos=0
    pmaior=np.array([0,0,0,0,0])
    for i5 in range(floor(a[4])+1):
        raiz3=max(0.0,1 -(i5**2/a[4]**2))
        a_4=a[3]*sqrt(raiz3)
        for i4 in range (floor(a_4)+1):
            raiz2= max(0.0,1 -(i4**2/a[3]**2)-(i5**2/a[4]**2))
            a_3=a[2]*sqrt(raiz2)
            for i3 in range (floor(a_3)+1):
                raiz1= max(0.0,1-(i3**2/a[2]**2) -(i4**2/a[3]**2)-(i5**2/a[4]**2))
                a_1=a[0]*sqrt(raiz1)
                a_2=a[1]*sqrt(raiz1)
                
                if a_1!=0:
                    (kmax,pmaior,npontos)=relaxado(a_1,a_2,i3,i4,i5,c[0],c[1],c,kmax,pmaior,npontos)
                else:
                    pt=np.array([0,0,i3,i4,i5])
                    if pt@c>kmax:
                        pmaior=pt
                        kmax=pt@c

    
    return [pmaior,kmax,npontos]

columns=['A1','A2','A3','A4','A5','C1','C2','C3','C4','C5','Tempo','K max','Ponto','Dentro Elips','Nº pontos analisados']
ncasos=5
seed=74
pont=[]
res=[]
tim=[]
dentro=[]
totalpontos=[]

(ai,ci,aii,cii,aiii,ciii,aiiii,ciiii,aiiiii,ciiiii)=dados(seed,ncasos)
print(aiiiii)

for j in range (ncasos):
    print(j)
    print('a5=',aiiiii[j])
    a=np.array([ai[j], aii[j], aiii[j], aiiii[j], aiiiii[j]])
    c=np.array([ci[j], cii[j], ciii[j], ciiii[j], ciiiii[j]])
    init = time.perf_counter()
    (ponto,k,qtdpontos)=AL5D(a,c)
    endt = time.perf_counter()
    tim.append((endt-init))
    res.append(k)
    pont.append(ponto)
    totalpontos.append(qtdpontos)
    if ((ponto[4]**2/a[4]**2)+(ponto[3]**2/a[3]**2)+ (ponto[2]**2 / a[2]**2)+ (ponto[1]**2 / a[1]**2)+ (ponto[0]**2 / a[0]**2))<=1:
      dentro.append(1)
    else:
      dentro.append(0)

    df = pd.DataFrame(list(zip(ai,aii,aiii,aiiii,aiiiii,ci,cii,ciii,ciiii,ciiiii,tim,res,pont,dentro,totalpontos)), columns=columns)
    df.to_excel(r"C:\Users\lucas_mzj9txp\Desktop\AL5D.xlsx")