from gurobipy import *

# Patrpnes
Pc = {1:[1,2,3,9,10], 2:[2,3,7,10], 3:[1,2,22,30], 4: [1,3,4,6], 5:[1,4,3,22,10], 6:[19,31,27,10], 7:[1,30,18,10], 8: [36,35,28,1]}
modulos = [1,2,22,30,4, 1,2,9,10, 2,3,7,10]
students = {1: [1,2],2: [2,3],3: [1,3], 4:[1], 5:[3]}
modulos = set(modulos)
#Cursos
K = [1,2,3]
#conjunto de salas
R = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
#conjunto de clases
C = [1,2,3,4,5,6,7,8]
# Conjunto de estudiantes
#conjunto de clases que erequieren sala, dict de key class id y value la capacidad
C_r = [1,2,3,4,5,6,7,8]
# conjunto de clases que no requieren sala dict de key class id y value la capacidad
C_sr = []
C_rf = {1: set([1, 2, 4, 6]), 2: set([2, 3]), 3: set([1, 3, 4, 5]), 4: set([1,3,5]), 5: set([5, 6, 7, 11]), 6: set([7, 8]), 7: set([1, 8, 9, 10]), 8: set([13,12,11])}
#Curso 1 y 2 no pueden estar en la misma sala
Cd= [1,2]
Cd_room = [1,3]
## not overlap
Cd_notoverlap = [2,4]
#Cl conjunto de clases de la subparte
Cl = {1:[1, 2, 3],2:[2],3:[3,4],4:[5,6,7],5:[8]}
#Zw conjunto de subpartes de del curso k
Zw = {1:[1,2, 4], 2:[3], 3:[4,5]}
#Sk conjunto de estudiantes que deben asistir al curso k
Sk = {1:[1, 3, 4],2:[1, 2 ],3:[2, 3, 5]}
parents = {2: [1]}
class_limit = {1: 10,2:10,3:10,4:10,5: 10,6: 10 ,7:10 ,8:10}

m=Model("mip1")

##creación de variable Xcrp
"""x_cpr=dict()
for c in C_r:
    for p in Pc[c]:
        for r in C_rf[c]:    
            x_cpr[c,p,r] = m.addVar( vtype=GRB.BINARY, name="xc=" + str(c) + ";p="  +str(p) + ";r" + str(r))
"""
##Creacion de variable Ycs, hacer forma mas eficiente entregando id de estudiante entregar cursos posible
y_sc=dict()
for s in students:
    for c in C_r:
        y_sc[s,c] = m.addVar( vtype=GRB.BINARY, name="ys=" + str(s) + ";c="  +str(c) ) 
        
"""b_sw = dict()
for s in students:
    for w in Zw:
         y_sc[s,w] = m.addVar( vtype=GRB.BINARY, name="bs=" + str(s) + ";w="  +str(w) )  """               
 
m.update()
m.setObjective(GRB.MINIMIZE)

#Restricciones de estudiantes
#1. Los estudiantes deben asistir a una clase de la subparte
for s in students:
    for k in K:
        if k in students[s]:
            for subparte in Zw[k]:
                m.addConstr(quicksum(y_sc[s,c] for c in Cl[subparte]) == 1) 
            
#4. Numero de alumnos que asisten a n la clase no puede exceder la capacidad de la clase.
# Class_id en gurobi como -> C 
for c in C_r:
    m.addConstr(quicksum(y_sc[s,c] for s in students) <= class_limit[c])            
                
#5. Si el alumno asite a un a clase que tiene una clase padre, entonces tambien debe asitir a la clase padre
for s in students:
    for ci in C_r:
        if ci in parents.keys():
            for cj in parents[ci]:
                m.addConstr(y_sc[s,ci] <= y_sc[s,cj]) 
    

                
# for s in students:
#     for k in K:
#         if k in students[k]:
#             m.addConstr(quicksum(b_sw[s,w] for w in Zw[k]) == 1)


'''
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
# for ci in Cd:
#     for cj in Cd:
#         for n in modulos:
#             if ci != cj:
#                 m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj] ) ) 

#Restriccion 6: Overlap, clases se solapan 
# for ci in Cd:
#     for cj in Cd:
#         for n in modulos:
#             if ci != cj:
#                 m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj]) ) 

#Restriccion 8: notOverlap, clases se solapan 
# for ci in Cd_notoverlap:
#     for cj in Cd_notoverlap:
#         for n in modulos:
#             if ci != cj:
#                 m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if  n in Pc[ci] ) + quicksum(x_cpr[cj,n,r] for r in C_rf[cj] for  p in Pc[cj] if p != n and  n in Pc[cj]) <= 1) 


 
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
'''
m.optimize()

for v in m.getVars():
   
    if v.x != 0:
        print(v.varName, v.x)
