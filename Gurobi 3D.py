from gurobipy import *
import time
import pandas as pd
import numpy as np
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

def Gurobi3D(a1,a2,a3,c1,c2,c3):
  elipse_model = Model("elipse")
  elipse_model.setParam('OutputFlag', 0)


  x1 = elipse_model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name="x1")#criando variavel x1
  x2 = elipse_model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name="x2")#criando variavel x2
  x3 = elipse_model.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name="x3")#criando variavel x2
  elipse_model.update()

  elipse_model.setObjective(c1 * x1 + c2 * x2 +c3*x3, GRB.MAXIMIZE)#criando objetivo(maximizar k)

  elipse_model.addQConstr((x1**2)/(a1**2) + (x2**2)/(a2**2) +(x3**2)/(a3**2) <= 1, name="elipse")#criando restrição(dentro da elipse)

  elipse_model.update()
  elipse_model.optimize()


  if elipse_model.Status == GRB.OPTIMAL:
    return (np.array([x1.X, x2.X,x3.X]))
  else:
    return None
  

columns=['A1','A2','A3','C1','C2','C3','Tempo','K max','Ponto','Dentro Elips']
ncasos=1000
seed=74
pont=[]
res=[]
tim=[]
dentro=[]

(ai,ci,aii,cii,aiii,ciii,aiiii,ciiii,aiiiii,ciiiii)=dados(seed,ncasos)

for j in range (ncasos):
    print(j)
    a=np.array([ai[j], aii[j],aiii[j]])
    c=np.array([ci[j], cii[j],ciii[j]])
    init = time.perf_counter()
    (ponto)=Gurobi3D(a[0],a[1],a[2],c[0],c[1],c[2])
    endt = time.perf_counter()
    tim.append((endt-init))
    res.append(ponto@c)
    pont.append(ponto)

    if ((ponto[2]**2 / a[2]**2)+ (ponto[1]**2 / a[1]**2)+ (ponto[0]**2 / a[0]**2))<=1:
      dentro.append(1)
    else:
      dentro.append(0)

    df = pd.DataFrame(list(zip(ai,aii,aiii,ci,cii,ciii,tim,res,pont,dentro)), columns=columns)
    df.to_excel(r"C:\Users\lucas_mzj9txp\Desktop\Gurobi3D.xlsx")