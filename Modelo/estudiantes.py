from gurobipy import *
from conjuntos2 import *
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
students = students
#Zw conjunto de subpartes de la configuración/curso -> Se llama zw
#Cl conjunto de clases de la subparte
#Parent conjunto de classes con sus respectivos padres

############################## MODELO ESTUDIANTES ############################

m=Model("modelo estudiantes")

#Creacion de variable ysc, toma 1 si el estudiante s toma el curso
y_sc=dict()
for s in students:
    for c in range(1, 536):
        y_sc[s,c] = m.addVar( vtype=GRB.BINARY, name="ys=" + str(s) + ";c="  +str(c) ) 


           

m.update()
m.setObjective(GRB.MINIMIZE)
##############################RESTRICCIONES####################################

#1. Los estudiantes deben asistir a una clase de la subparte
for s in students:
    for k in K:
        if k in students[s]:
            for subparte in zw[k]:
                try:
                    m.addConstr(quicksum(y_sc[s,c] for c in cl[subparte]) == 1) 
                except:
                    pass

#4. Numero de alumnos que asisten a n la clase no puede exceder la capacidad de la clase.
# Class_id en gurobi como -> C 
for c in C:
    m.addConstr(quicksum(y_sc[s,c] for s in students) <= class_limit[c])            
                
#5. Si el alumno asite a un a clase que tiene una clase padre, entonces tambien debe asitir a la clase padre
for s in students:
    for ci in C:
        if ci in parent.keys():
                m.addConstr(y_sc[s,ci] <= y_sc[s,parent[ci]]) 
    

m.optimize()

var_names = []

for var in m.getVars():
     if var.x != 0:
        
        print(var.varName, var.x)




