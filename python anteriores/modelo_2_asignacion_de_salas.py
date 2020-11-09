from gurobipy import *
from conjuntos2 import *
import numpy as np


Rc=salas_factibles #diccionario de clases que requieren sala con el formato {llave de la clase: lista de salas factibles clase}
Cr=class_id #lista de id de clases que requieren salas
C=c_id #lista de id de clases de todas las clases
Sc=bloques_clase#diccionario de clases que indica sus bloques posibles con el formato {llave de la clase: lista de horarios factibles clase}

numero_clases_instancia_con_sala=len(Cr)
numero_clases_instancia=len(C)

#formaremos el conjunto Vc en una lista de listas por ahora ( no sirvio :( )
# Vc=[]
# for c in C[0:13]:
#     clasec=[]
#     for s in range(len(Sc[c])):
#         for v in range(len(Sc[c][s][1])):
#             if (str(Sc[c][s][0])+str(Sc[c][s][1][v])) not in clasec:
#                 clasec.append(str(Sc[c][s][0])+str(Sc[c][s][1][v]))
#     Vc.append(clasec)
#ahora se creará un subconjunto para las patrones que tienen tope de horario con el patrón i
# tope=[]
# for cf in Cr[0:numero_clases_instancia_con_sala]:
#     clase=[]
#     for s in range(len(Sc[cf])):#Sc[4] = [['L', [7, 8, 9, 10, 11]], ['M', [7, 8, 9, 10, 11]], ['W', [7, 8, 9, 10, 11]],...]
#         patron=[]
#         dia=Sc[cf][s][0] #asi s tomas los valores s = ['L', [7, 8, 9, 10, 11]]  , despues s = ['M', [7, 8, 9, 10, 11]] , etc
#         modulos=Sc[cf][s][1]
#         #ahora debo ir revisando en todos los patrones y agrego si hay traslape
#         for cprueba in Cr[0:numero_clases_instancia_con_sala]:
#             for sprueba in range(len(Sc[cprueba])):
#                 if (dia==Sc[cprueba][sprueba][0]):
#                     contador=0
#                     for m in (Sc[cprueba][sprueba][1]):
#                         if (m in modulos) and (contador==0):#quiere decir que hay calce de horarios
#                              if (cf!=cprueba) or (s!=sprueba):
#                                 patron.append([cprueba,sprueba])
#                                 contador=contador+1
#         clase.append(patron)
#     tope.append(clase)












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

#se crean las variables

m=Model("mip1")
y_cvs={}
for c in C[0:numero_clases_instancia]:
    for s in range(len(Sc[c])):#sub indice s es el numero de patron horario factible para clase c.
        for v in (Sc[c][s][1]):#sub indice v es el numero de modulo del patron s factible para clase c.
            y_cvs[c,v,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="Yc=" + str(c) + ";v=" + Sc[c][s][0]+str(v) + ";s" + str(s))
           
yr_crs={}
for c in Cr[0:numero_clases_instancia_con_sala]:
    for r in Rc[c]:#sub indice r es id de la sala factible para la clase s.
        for s in range(len(Sc[c])): #sub indice s es el numero de patron horario factible para clase c.
            yr_crs[c,r,s] = m.addVar(obj=1, vtype=GRB.BINARY, name="Yrc=" + str(c) + ";r=" + str(r) + ";s=" + str(s))


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
        vi=Sc[c][s][1][0]
        nvc=len(Sc[c][s][1])
        m.addConstr(quicksum(y_cvs[c, v, s] for v in (Sc[c][s][1][1:]))-(nvc-1)*y_cvs[c, vi, s]==0)










#     for c in C:
#         for so in SO:
#             for so in sdnvc:
#                 for vi in initc:
#                     nvc=5
#                     nvc=dict....aqui se debe reconocer el parametro nvc
#                     m.addConstr(quicksum(y_cvs[c,v,s] for v in range(vi+1,vi+nvc) for s in range(so+1,so+nvc)) -(nvc-1)*y_cvs[c,vi,so] == 0)

# restriccion 7: No tener superposicion horaria para las salas, un curso en la sala en ese bloque
# for r in R:
#     for s in Sc[]:
#         m.addConstr(quicksum(yr_crs[c,r,Sc[c][s][1][i]] for c in C for r in R) <= 1)

#restriccion 7: No tener superposicion horaria para las salas, un curso en la sala en ese bloque


# count=-1
# for c in Cr[0:numero_clases_instancia_con_sala]:
#     count+=1   
#     for s in range(len(Sc[c])):
#         for r in Rc[c]:
#             a = yr_crs[c, r, s]
#             for lista in tope[count][s]:
#                 if r in Rc[lista[0]]:
#                     a=a+yr_crs[lista[0],r,lista[1]]
#             m.addConstr(a<=1)

#Version 2 restriccion 7

for r in Rc:
 #Dudoso no sabemos si parten    
    for v in range(1,25):
        try:
            m.addConstr(quicksum(yr_crs[c,r,v] for c in Cr[0:numero_clases_instancia_con_sala]) <= 1)
        except KeyError as e:
            pass
            













        #ahora reviso en los conjuntos c,s con tope para el c y el s actual, procurando revisar si r es factible para el







#restriccion 8: Asignar sala a una clase en un bloque horario determinada

for c in Cr[0:numero_clases_instancia_con_sala]: #estas son las clases que requieren sala
    for s in range(len(Sc[c])):
        try:

            m.addConstr(quicksum(yr_crs[c,r,s] for r in (Rc[c])) == y_cvs[c,Sc[c][s][1][0],s])
        except KeyError as e:
            pass 



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
#for v in m.getVars():
 #   if v.x==0:
        #print('%s %g' % (v.varName, v.x))
# #print(S)
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
# for i in range(20):
#     print(Sc[i+1])
# for i in Cr[0:20]:
#     print("salas clase",i,":")
#     print(Rc[i])

# for c in C[0:numero_clases_instancia]:
#     print("patrones clase ",c )
#     print(Sc[c])


