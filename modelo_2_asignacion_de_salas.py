from gurobipy import *
from conjuntos import *
import numpy as np
m=Model("mip1")
D=range(7)
SO=range(2)
Sd=range(58)
S=bloques
S1=range(2)
S2=range(2)
#nvc=duracion_clase
#Rc=range(2)

Rc=salas_factibles #diccionario de clases que requieren sala con el formato {llave de la clase: lista de salas factibles clase}
Cr=class_id #lista de id de clases que requieren salas
C=c_id#lista de id de clases de todas las clases
M=range(8)
lecM=range(6)
A=range(10)
#V=range(20)
#Vc=range(2)
Sc=bloques_clase#diccionario de clases que indica sus bloques posibles con el formato {llave de la clase: lista de horarios factibles clase}
initc=range(2)
slot=range(10)
sdnvc=range(3)
numero_clases_instancia=10
# print(Sc[296])
# print(Sc[297])
# print(Sc[350])
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
for c in C[0:numero_clases_instancia]:
    for s in range(len(Sc[c])):#sub indice s es el numero de patron horario factible para clase c.
        for v in (Sc[c][s][1]):#sub indice v es el numero de modulo del patron s factible para clase c.
            y_cvs[c,v,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="Yc=" + str(c) + ";v=" + Sc[c][s][0]+str(v) + ";s" + str(s))
# yr_crs={}
# for c in Cr[0:numero_clases_instancia]:
#     for r in Rc[c]:#sub indice r es id de la sala factible para la clase s.
#         for s in range(len(Sc[c])): #sub indice s es el numero de patron horario factible para clase c.
#             yr_crs[c,r,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="Yrc=" + str(c) + ";r=" + str(r) + ";s=" + str(s))

yr_crv={}
for c in Cr[0:numero_clases_instancia]:
    for r in Rc[c]:#sub indice r es id de la sala factible para la clase s.
        for v in (Vc[c]) #sub indice s es el numero de patron horario factible para clase c.
            yr_crv[c,r,v] = m.addVar(obj=1, vtype=GRB.BINARY, name="Yrc=" + str(c) + ";r=" + str(r) + ";v=" + str(v))








m.update()
m.ModelSense = GRB.MINIMIZE

#tambien se puede setear el objetivo como m.setObjective(ACA VA LA F.O. que sera enorme, GRB.MINIMIZE)
#restriccion 1

#restriccion 3: programar eventos de una clase en exactamente un bloque horario entre los factibles
for c in C[0:numero_clases_instancia]:
    m.addConstr(quicksum(y_cvs[c,Sc[c][s][1][0],s] for s in range(len(Sc[c]))) == 1)
    #para cada clase, se revisa que la suma de los primeros modulos de todos los patrones posibles sea 1 (se asigna dicho patron)


#restriccion 4: Asignar la frecuencia semanal.
# v=1 #aca se asume que v=1 es un modulo con codigo 1, pero depende de cada c
# for d in D:
#     for c in C:
#         m.addConstr(quicksum(y_cvs[c,v,s] for s in S) <= 1)
# # restriccion 5: Los eventos de un mismo dia son consecutivo
for c in C[0:numero_clases_instancia]:
    for s in range(len(Sc[c])):
        # print(len(Sc[c]))
        # print("c=",c)
        # print(Sc[c])
        vi=Sc[c][s][1][0]
        nvc=len(Sc[c][s][1])
        #print("Scc=",c,"s=",s)
        #print(Sc[c][s][1])
        #print(Sc[c][s][1][1:])
        m.addConstr(quicksum(y_cvs[c, v, s] for v in (Sc[c][s][1][1:]))-(nvc-1)*y_cvs[c, vi, s]==0)










#     for c in C:
#         for so in SO:
#             for so in sdnvc:
#                 for vi in initc:
#                     nvc=5
#                     nvc=dict....aqui se debe reconocer el parametro nvc
#                     m.addConstr(quicksum(y_cvs[c,v,s] for v in range(vi+1,vi+nvc) for s in range(so+1,so+nvc)) -(nvc-1)*y_cvs[c,vi,so] == 0)
# restriccion 7: No tener superposicion horaria para las salas, un curso en la sala en ese bloque
for r in R:
    for s in Sc[]:
        m.addConstr(quicksum(yr_crs[c,r,Sc[c][s][1][i]] for c in C for r in R) <= 1)


#restriccion 8: Asignar sala a una clase en un bloque horario determinada

# for c in Cr[0:6]: #estas son las clases que requieren sala
#      for s in range(len(Sc[c])):
#          m.addConstr(quicksum(yr_crs[c,r,s] for r in (Rc[c])) == y_cvs[c,Sc[c][s][1][0],s])
# #        m.addConstr(quicksum(yr_crs[c,r,s] for r in (Rc[c])) == quicksum(y_cvs[c,v,s] for v in (Sc[c][s][1])))
# #




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

for v in m.getVars():
    if v.x==1:
        print('%s %g' % (v.varName, v.x))
for v in m.getVars():
    if v.x==0:
        print('%s %g' % (v.varName, v.x))
#print(S)
#para obtener el valor de una varibla particular:
# for v in m.getVars():
#     if v.varName=="yc1v1s1":
#         print(v.varName, v.x)

# print(C[0])
# print(V[1])
# print(V[40])
# print(Cr[0:10])
# print(Rc)
# print(Rc[272])
# print(Sc[4])
# print(len(Sc[4][1][1]))
#print(C)
