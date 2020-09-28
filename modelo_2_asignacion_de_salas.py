from gurobipy import *
from conjuntos import *
import numpy as np
m=Model("mip1")
D=range(7)
SO=range(2)
Sd=range(58)
S=range(20)
S1=range(2)
S2=range(2)
Rc=range(2)
Sc=range(4)
R=range(20)
#C=range(10)
C=c_id
M=range(8)
lecM=range(6)
A=range(10)
#V=range(20)
#Vc=range(2)
Sc=bloques_clase
initc=range(2)
slot=range(10)
sdnvc=range(3)

# x_ac={}
# for a in C:
#     for c in A:
#         x_ac[a,c]=m.addVar(obj=1, vtype=GRB.BINARY,name="xa"+str(a)+"c"+str(c))
# xs_acs={}
# for a in C:
#     for c in A:
#         for s in S:
#             xs_acs[a,c,s]=m.addVar(obj=-1, vtype=GRB.BINARY,name="xsa"+str(a)+"c"+str(c)+"s"+str(s))
y_cvs={}
for c in C:
    for v in range(len(Sc[c][0][1])):#revisar otras clases
        for s in S:
            y_cvs[c,v,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="yc" + str(c) + "v" + str(v) + "s" + str(s))
# yr_crs={}
# for c in C:
#     for r in R:
#         for s in S:
#             yr_crs[c,r,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="yrc" + str(c) + "r" + str(r) + "s" + str(s))

m.update()
m.ModelSense = GRB.MINIMIZE

#tambien se puede setear el objetivo como m.setObjective(ACA VA LA F.O. que sera enorme, GRB.MINIMIZE)
#restriccion 1

#restriccion 3 (OK): programar eventos de una clase en exactamente un bloque horario entre los factibles
#for c in C:
    #for v in range(len(V[c][0][1])):
        #m.addConstr(quicksum(y_cvs[c,v,s] for s in SO) == 1)#es un Sc en realidad

for c in C:
    for v in range(len(V[c][0][1])):
        m.addConstr(quicksum(y_cvs[c,v,s] for s in S0) == 1) #es un Sc en realidad


#restriccion 4: Asignar la frecuencia semanal.
# v=1 #aca se asume que v=1 es un modulo con codigo 1, pero depende de cada c
# for d in D:
#     for c in C:
#         m.addConstr(quicksum(y_cvs[c,v,s] for s in S) <= 1)
# # restriccion 5: Los eventos de un mismo dia son consecutivo
# # for d in D:
# #     for c in C:
# #         for so in SO:
# #             for so in sdnvc:
# #                 for vi in initc:
# #                     nvc=5
# #                     nvc=dict....aqui se debe reconocer el parametro nvc
# #                     m.addConstr(quicksum(y_cvs[c,v,s] for v in range(vi+1,vi+nvc) for s in range(so+1,so+nvc)) -(nvc-1)*y_cvs[c,vi,so] == 0)
# # restriccion 7: No tener superposicion horaria para las salas, un curso en la sala en ese bloque
# for r in R:
#     for s in S:
#         m.addConstr(quicksum(yr_crs[c,r,s] for c in C for r in R) <= 1)
# # #restriccion 8: Asignar sala a una clase en un bloque horario determinada
# for c in C:
#     for s in S:
#         m.addConstr((quicksum(yr_crs[c,r,s] for r in R)) == (quicksum(y_cvs[c,v,s] for v in V)))
# # #resgtriccion 9: No hay cambio de sala dentro de un mismo dia
# #
# #
# for c in C:
#     for so in SO:
#         for so in sdnvc:
#             for vi in initc:
#                 for r in Rc:
#                     nvc=5
#                     #nvc=dict....aqui se debe reconocer el parametro nvc
#                     m.addConstr(quicksum(yr_crs[c,r,s] for s in range(so+1,so+nvc))>=(nvc-1)*(y_cvs[c,vi,so]+yr_crs[c,r,so]-1))
#
#
# #restriccion 10: No tener tope de horario entre las clases asignados al alumno
# for a in A:
#     for s in S:
#         m.addConstr(quicksum(xs_acs[a,c,s] for c in C for m in M) <= 1)
#restriccion 11: relacionar variables
# for c in C:
#     for v in V:
#         for s in S:
#             for a in A:
#                 #for m M: tenemos que activarlo cuando hagamos bien los subconjuntos
#                 m.addConstr(y_cvs[c,v,s]+x_ac[a,c]-xs_acs[a,c,s] <= 1)
#
# #restriccion 12: relacionar variables
# for a in A:
#     for c in C:
#         for s in S:
#             #for m in M:tenemos que activarlo cuando hagamos bien los subconjuntos
#             m.addConstr(2*xs_acs[a,c,s]-(quicksum(y_cvs[c,v,s] for v in V)-x_ac[a,c])<=0)

m.optimize()

#para obtener las variables que son iguales a un valor


#imprime todas las variables
#for v in m.getVars():
    #print('%s %g' % (v.varName, v.x))

# for v in m.getVars():
#     if v.x==0:
#         print('%s %g' % (v.varName, v.x))

#para obtener el valor de una varibla particular:
# for v in m.getVars():
#     if v.varName=="yc1v1s1":
#         print(v.varName, v.x)

print(C[0])
print(V[1])
print(V[40])


