from gurobipy import *

# Patrpnes
Pc = {1:[1,2,3,9,10], 2:[2,3,7,10], 3:[1,2,22,30], 4: [1,3,4,6]}
modulos = [1,2,22,30,4, 1,2,9,10, 2,3,7,10]
modulos = set(modulos)
#conjunto de salas
R = [1,2,3,4,5,6]
#conjunto de clases
C = [1,2,3]
# Conjunto de estudiantes
#conjunto de clases que erequieren sala, dict de key class id y value la capacidad
C_r = [1, 2, 3]
# conjunto de clases que no requieren sala dict de key class id y value la capacidad
C_sr = []
C_rf = {1: set([1, 2, 4, 6]), 2: set([2, 3]), 3: set([1, 3, 4, 5]), 4: set([1,3,5])}
#Curso 1 y 2 no pueden estar en la misma sala
Cd= [1,2]
Cd_room = [1,3]
## not overlap
Cd_notoverlap = [2,4]

m=Model("mip1")

##creación de variable Xcrp
x_cpr=dict()
for c in C_r:
    for p in Pc[c]:
        for r in C_rf[c]:    
            x_cpr[c,p,r] = m.addVar( vtype=GRB.BINARY, name="xc" + str(c) + ";p="  +str(p) + ";r" + str(r))
 
m.update()
m.setObjective(GRB.MINIMIZE)



# #restricción 1: asignar un patron factible a la clase c con cierta sala
#Esta restriccion toma el primer patron
for c in C_r: #estas son las clases que requieren sala 
  
    m.addConstr(quicksum(x_cpr[c,p,r] for r in C_rf[c] for p in Pc[c] ) == 1) 


# restricción 2:  cada sala puede tener solo 1 clase en cada m ́odulo


for r in R:
    for n in modulos:
            m.addConstr(quicksum(x_cpr[c,n,r] for c in C_r if r in C_rf[c] and n in Pc[c])  <= 1) 
       
    
#Restricción 3: dos clases no pueden colocarse en la misma sala

# Samestart/Sametime , Samedays, Noverlap, Overlap, SameAttendes, Precedence
#Restriccion 5: SAMESTART , que partan al mismo horario
for ci in Cd:
    for cj in Cd:
        for n in modulos:
            if ci != cj:
                m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj] ) ) 

#Restriccion 6: Overlap, clases se solapan 
for ci in Cd:
    for cj in Cd:
        for n in modulos:
            if ci != cj:
                m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj]) ) 

#Restriccion 8: notOverlap, clases se solapan 
for ci in Cd_notoverlap:
    for cj in Cd_notoverlap:
        for n in modulos:
            if ci != cj:
                m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if  n in Pc[ci] ) + quicksum(x_cpr[cj,n,r] for r in C_rf[cj] for  p in Pc[cj] if p != n and  n in Pc[cj]) <= 1) 


 
#Restriccion 4:  Same Room que tienen que estar en la misma sala   

#for ci in Cd_room:
 #   for cj in Cd_room:
  #      if ci != cj:
   #         for ri in R_cf:
    #            print(ri)
     #           m.addConstr(quicksum(x_cpr[ci,n,ri] for n in Pc[ci]) == quicksum(x_cpr[cj,n,ri] for n in Pc[cj]))       

#m.feasRelaxS(0, True, False, True)
#m.setParam(GRB.Param.InfUnbdInfo, 1)
#m.setParam(GRB.Param.heuristics, 0.5)
m.optimize()

for v in m.getVars():
   
    if v.x != 0:
        print(v.varName, v.x)
