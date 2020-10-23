from gurobipy import *
from conjuntos_new import *
import numpy as np
## se definen los conjuntos de la manera presentada en el informe
#conjunto de patrones
Pc = patterns

#conjunto de salas
R = rooms
#conjunto de clases
C = class_limit.keys()
# Conjunto de estudiantes
#E = 
#conjunto de cursos
K = courses
#conjunto de clases que erequieren sala, dict de key class id y value la capacidad
C_r = classes_room
# conjunto de clases que no requieren sala dict de key class id y value la capacidad
C_sr = classes_no_room

C_rf = salas_factibles
#Cursos que tienen same start
Cd = same_start_conjunto


m=Model("mip1")
##creación de variable xcpr
x_cpr=dict()
for c in C_r:
    try:
        for p in Pc[c]:
            

            for r in C_rf[c]:
                
                x_cpr[c,p,r] = m.addVar( vtype=GRB.BINARY, name="xc" + str(c) + ";p="  +str(p) + ";r" + str(r))
    except:
        pass     

m.update()
m.setObjective(GRB.MINIMIZE)


#restricción 1: asignar un patron factible a la clase c con cierta sala
for c in C_r: #estas son las clases que requieren sala 
  
    try:
   
      
        m.addConstr(quicksum(x_cpr[c,p,r] for r in C_rf[c] for p in Pc[c] ) == 1) 
    except:
        pass

# restricción 2:  cada sala puede tener solo 1 clase en cada m ́odulo
for r in R:
    for n in range(1, 43):
            m.addConstr(quicksum(x_cpr[c,n,r] for c in C_r if r in C_rf[c] and n in Pc[c])  <= 1)

#Restriccion 5: SAMESTART, que partan al mismo horario

for l in Cd:
    for ci in l:
        for cj in l:
            for n in modulos:
    #           for nj in Pc[cj]:
                if ci != cj:
    #               if n in Pc[ci] and n in Pc[cj]:
                        m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj])) 

#m.feasRelaxS(0, True, False, True)
#m.setParam(GRB.Param.InfUnbdInfo, 1)
#m.setParam(GRB.Param.heuristics, 0.5)
#print(len(C_r))
m.optimize()

for v in m.getVars():
  
    if v.x != 0:
        print(v.varName, v.x)