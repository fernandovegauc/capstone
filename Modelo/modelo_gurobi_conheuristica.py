from gurobipy import *
from conjuntos2_heuristica import *
import numpy as np
import csv
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
##Cd = same_start_conjunto
#cursos que tienen overlap
#Cd_overlap = overlap
#Conjunto de estudiantes que contiene el ID del estudiante y los cursos que debe tomas son los value
Students = students
#Zw conjunto de subpartes de la configuración
#Cl conjunto de clases de la subparte
print(C_sr)


Cd_notoverlap = [[]]

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

for y in C_sr:
    x_cpr[y,C_sr[y],4000] = m.addVar( vtype=GRB.BINARY, name="xc" + str(c) + ";p="  +str(p) + ";r" + str(r))


    
#Creacion de variable ysc, toma 1 si el estudiante s toma el curso
#antes descomentada
# y_sc=dict()
# for s in Students:
#     for c in C_r:
#         y_sc[s,c] = m.addVar( vtype=GRB.BINARY, name="ys=" + str(s) + ";c="  +str(c) )

m.update()
m.setObjective(GRB.MINIMIZE)

##restriccion 0 : asiganr clases sin salas
for y in C_sr:
    m.addConstr(x_cpr[y,C_sr[y],4000] == 1) 



#restricción 1: asignar un patron factible a la clase c con cierta sala
for c in C_r: #estas son las clases que requieren sala 
  
   
   
      
    m.addConstr(quicksum(x_cpr[c,p,r] for r in C_rf[c] for p in Pc[c] ) == 1) 


# restricción 2:  cada sala puede tener solo 1 clase en cada m ́odulo
for r in R:
    for n in range(1, 84):
        try:
            m.addConstr(quicksum(x_cpr[c,n,r] for c in C_r if r in C_rf[c] and n in Pc[c])  <= 1)
        except:
            pass
#Restriccion 5: SAMESTART, que partan al mismo horario
'''
for l in Cd:
    for ci in l:
        for cj in l:
            for n in modulos:
    #           for nj in Pc[cj]:
                if ci != cj:
    #               if n in Pc[ci] and n in Pc[cj]:
                        m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj])) 
#Restriccion 7: Overlap

for l in Cd_overlap:
    for ci in l:
        for cj in l:
            for n in modulos:
    #           for nj in Pc[cj]:
                if ci != cj:
    #               if n in Pc[ci] and n in Pc[cj]:
                        m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if n in Pc[ci]) == quicksum(x_cpr[cj,n,r]for r in C_rf[cj] if n in Pc[cj])) 



#Restriccion 8: notOverlap, clases se solapan 
for x in Cd_notoverlap:
    for ci in x:
        
        for cj in x:
            for n in modulos:
                if ci != cj:
                    m.addConstr(quicksum(x_cpr[ci,n,r] for r in C_rf[ci] if  n in Pc[ci] ) + quicksum(x_cpr[cj,n,r] for r in C_rf[cj] for  p in Pc[cj] if p != n and  n in Pc[cj]) <= 1) 

'''
 
#m.feasRelaxS(0, True, False, True)
#m.setParam(GRB.Param.InfUnbdInfo, 1)
#m.setParam(GRB.Param.heuristics, 0.5)
#print(len(C_r))
m.optimize()

# for v in m.getVars():
#     if v.x != 0

def devuelve_dia(modulo):
    original=[]
    if modulo<=7:
        return "L"
    elif modulo <=14:
        return "M"
    elif modulo <=21:
        return "W"
    elif modulo <= 28:
        return "J"
    elif modulo <= 35:
        return "V"
    elif modulo <= 42:
        return "S"
    else:
        return "D"


def devuelve_start(modulo):
    if modulo in [1,8,15,22,29,36,43]:
        return 96
    elif modulo-1 in [1,8,15,22,29,36,43]:
        return 120
    elif modulo - 2 in [1, 8, 15, 22, 29, 36, 43]:
        return 144
    elif modulo - 3 in [1, 8, 15, 22, 29, 36, 43]:
        return 168
    elif modulo - 4 in [1, 8, 15, 22, 29, 36, 43]:
        return 192
    elif modulo - 5 in [1, 8, 15, 22, 29, 36, 43]:
        return 216
    else:
        return 240


asignado=list()
asignado_con_clase=list()
#respuestaxs de gurobi se pasan a lista asignados
for key in x_cpr:
    #print(key, ":",x_cpr[key],":",type(x_cpr[key].x))
    if (x_cpr[key].x)==1: #valor de la variable es 1 (se asigna)
        asignado.append([key[2],devuelve_dia(key[1]),devuelve_start(key[1]),devuelve_start(key[1])+22-1])#[id_sala,día,slot_start,slot_end]
        asignado_con_clase.append([key[0],key[2],devuelve_dia(key[1]),devuelve_start(key[1]),devuelve_start(key[1])+22-1])#[id_clase, id_sala,día,slot_start,slot_end]
ahora=len(asignado)
#todas las clases de largo 22 han sido asignadas de forma optima y guardadas en asignado con clase con formato:
#[id_clase,id_sala,día,slot_start,slot_end]
#A continuación se comienza a asignar mediente heurística de asignación

# #*Heuristica******************************************************************************************************************************
# #*********************************************************************************************************************************************



#iniciamos con clases de largo 34

def notraslape(A,B):
    for patron in B:
        if (A[0]==patron[0]) and (A[1]==patron[1]): #misma sala y mismo dia
            if (A[2]<=patron[3]) and (A[3]>=patron[2]): #cagamos hay tope
                return False
    return True
##########################################
cuenta34=0
for i in patterns34:
    listo=0
    for opcion in patterns34[i]: #opcion es ['M', 96, 129] por ejemplo
        try:
            for s in salas_factibles_heu[i]:#[s]+opcion=[sala18, "J", slot_ini90,slotfin_99]
                if listo==0 and (notraslape([s]+opcion,asignado)):#asignado=[[sala18, "J", slot_ini90,slotfin_99],[sala156, "V", slot_ini13,slotfin_99]]
                    cuenta34=cuenta34+1
                    asignado.append([s]+opcion)
                    asignado_con_clase.append([i]+[s]+opcion)
                    listo=1
        except:
            pass
cuenta10=0
for i in patterns10:
    listo=0
    for opcion in patterns10[i]: #opcion es ['M', 96, 129] por ejemplo
        try:
            for s in salas_factibles_heu[i]:
                if listo==0 and (notraslape([s]+opcion,asignado)):
                    cuenta10=cuenta10+1
                    asignado.append([s]+opcion)
                    asignado_con_clase.append([i]+[s]+opcion)
                    listo=1
        except:
            pass
cuenta46=0
for i in patterns46:
    listo=0
    for opcion in patterns46[i]: #opcion es ['M', 96, 129] por ejemplo
        try:
            for s in salas_factibles_heu[i]:
                if listo==0 and (notraslape([s]+opcion,asignado)):
                    cuenta46=cuenta46+1
                    asignado.append([s]+opcion)
                    asignado_con_clase.append([i]+[s]+opcion)
                    listo=1
        except:
            pass
cuenta58 = 0
for i in patterns58:
    listo=0
    for opcion in patterns58[i]: #opcion es ['M', 96, 129] por ejemplo
        try:
            for s in salas_factibles_heu[i]:
                if listo==0 and (notraslape([s]+opcion,asignado)):
                    cuenta58=cuenta58+1
                    asignado.append([s]+opcion)
                    asignado_con_clase.append([i]+[s]+opcion)
                    listo=1
        except:
            pass

cuenta106 = 0
for i in patterns106:
    listo=0
    for opcion in patterns106[i]: #opcion es ['M', 96, 129] por ejemplo
        try:
            for s in salas_factibles_heu[i]:
                if listo==0 and (notraslape([s]+opcion,asignado)):
                    cuenta106=cuenta106+1
                    asignado.append([s]+opcion)
                    asignado_con_clase.append([i]+[s]+opcion)
                    listo=1
        except:
            pass
print("Numeros")
print(len(patterns10))
print(cuenta10)
print(len(patterns34))
print(cuenta34)
print(len(patterns46))
print(cuenta46)
print(len(patterns58))
print(cuenta58)
print(len(patterns106))
print(cuenta106)

print("numero clases asignadas")
print(len(asignado))

#Algoritmo heuristica de asignacion clases con 1 patron factible
#las clases_room es la salas es la key y el value es su capacidad
#rooms de entra por id de la sala y devuelve su capacidad
cuenta=0
for i in one_pattern: #i=12 (la clase 12 solo tiene un patron factible)
    listo=0
    for s in salas_factibles_heu[i]: #salas_factibles[12]=[1,4,5] luego s = 1,4,5
        if listo == 0 and (notraslape([s] + one_pattern[i], asignado)):
            asignado.append([s] + one_pattern[i])
            asignado_con_clase.append([i] + [s] + one_pattern[i] )
            listo = 1
            cuenta=cuenta+1

# #algoritmo asignación de cursos con 1 sala factible.
cuenta1=0
for i in one_room: #i=1 (la clase 1 solo tiene la sala 190 factible)
    listo=0
    pattern_ok = 0
    for p in one_room[i]: #p tomara todos los patrones de clase i
        if listo == 0 and (notraslape(p, asignado)):
            asignado.append(p)
            asignado_con_clase.append([i] + p)
            listo=1
            cuenta1=cuenta1+1

#
# print(len(patterns10))
# print(cuenta10)
# print(len(patterns34))
# print(cuenta34)
# print(len(patterns46))
# print(cuenta46)
# print(len(patterns58))
# print(cuenta58)
# print(len(patterns106))
# print(cuenta106)
# print(len(one_pattern))
# print(cuenta)
# print(len(one_room))
# print(cuenta1)
#
# print("numero clases asignadas")
# print(len(asignado))
# print(len(asignado)-ahora)









#
# var_names = []
#
# for var in m.getVars():
#     if var.x != 0:
#
#         print(var.varName, var.x)
#
# # Write to csv
# with open('testout.csv', 'w') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(zip(var_names))

