from gurobipy import *
from conjuntos_new import *
import numpy as np
## se definen los conjuntos de la manera presentada en el informe
#conjunto de modulos horarios
M = patterns
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



m=Model("mip1")
##creación de variable xcpr
x_cpr=dict()
for c in C_r:
    for p in M[c]:
        for r in C_rf[c]:
            x_cpr[c,p[1],r] = m.addVar( vtype=GRB.BINARY, name="xc" + str(c) + ";p="  +str(p[0])+"-"+ str(p[1]) + ";r" + str(r))
           

m.update()
m.setObjective(GRB.MINIMIZE)



#restricción 1: asignar un patron factible a la clase c con cierta sala
#for c in C_r: #estas son las clases que requieren sala
      
#    if M[c] != []:
#        try:
#            print('i am trying')
#            m.addConstr(quicksum(x_cpr[c,p,r] for r in C_rf[c] for p in M[c]) == 1) 
#        except:
#            pass


# restricción 2:  cada sala puede tener solo 1 clase en cada m ́odulo
#for r in R:
#    for p in M:
#        try:
            
 #           m.addConstr(quicksum(x_cpr[c,p,r] for c in C_r  == 1) )
 #       except:
 #           pass
            

for c in C_r:
    for p in M[c]:
        for r in R:
            try:
                m.addConstr(x_cpr[c,p,r]  == 1) 
            except:
                pass


m.optimize()

for v in m.getVars():
    
    print(v.varName, v.x)