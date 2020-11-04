import pandas as pd
import numpy as np
import xlrd
import math

#importar salas
room = pd.read_csv('muni-fi-fal-17/room_capacity.csv',delimiter=';')

#importar cursos
#cursos tiempo
courses_time = pd.read_csv('muni-fi-fal-17/cursos_tiempo.txt',delimiter=',')
#cursos con salas
courses_room = pd.read_csv('muni-fi-fal-17/cursos_sala.txt',delimiter=',')

#cursos con restricciones de distribución
distribucion = pd.read_csv('muni-fi-fal-17/rest_dist.csv',delimiter=';')

#estudiantes
estudiantes = pd.read_csv('muni-fi-fal-17/estudiantes.csv',delimiter=';')

#### conjuntos listos 
rooms = dict()
#creeación de conjunto de salas
for x in room.index:  
    rooms[room['id '][x]] = room['capacity'][x]

####Dividir cursos por semanas
Cursos_pares = courses_time[(courses_time['class_weeks'] == '0101010101010')]
Cursos_impares = courses_time[(courses_time['class_weeks'] == '1010101010101')]

##creamos las salas factibles para cada clase
salas_factibles = dict()
class_id = courses_room['class_id']
class_id = np.unique(class_id)
for x in class_id:
    salas_factibles[x] = []
for i in courses_room.index:
    salas_factibles[courses_room['class_id'][i]].append(courses_room['room_id'][i])

## diccionario con key class_id y el value es class_limit 
class_limit = dict()
for x in courses_time.index:
    class_limit[courses_time['class_id'][x]] = courses_time['class_limit'][x]

##las keys son los courses_id y por el momento el value es una lista vacía
courses = dict()
for x in courses_time.index:
    courses[courses_time['course_id'][x]] = []

##las clases que requieren salas es la key y el value es su capacidad
courses_true = courses_time[(courses_time['class_room'] != False)]
courses_true = courses_true.drop(['class_room'], axis = 1)
classes_room = dict()
for x in courses_true.index:
    classes_room[courses_true['class_id'][x]] = courses_true['class_limit'][x]

## las clases que no requieren salas, salas es la key y el value es su capacidad
courses_false = courses_time[(courses_time['class_room'] == False)]
courses_false = courses_false.drop(['class_room'], axis = 1)
classes_no_room = dict()
for x in courses_false.index:
    classes_no_room[courses_false['class_id'][x]] = courses_false['class_limit'][x]

##modulos horarios van del 1 al 6 parten en el 108 y terminan en en 252
modulos = dict()
count = 0
for i in range(1,13):
    modulos[i] = [96 + 12 * count , 108 + 12 * count]
    count += 1

## Cursos cacho con duracion 34 y 46, se hacen dos set
duration34 = set()
duration46 = set()
duration58 = set()
duration106 = set()
##conjunto de patrones factibles para la clase c que tiene SALA
patterns = dict()
#Rellenamos diccionarios con id de clases con sala
for i in classes_room.keys():
    patterns[i] = []


##función que cambia los numeros por letras
def days_function(semana):
    if semana ==  1000000:
        day = 'L'
        return 1
    if semana == 100000:
        day = 'M'
        return 2
    if  semana == 10000:
        day = 3
        return day
    if semana == 1000:
        day = 4
        return day
    if semana == 100:
        day = 5
        return day
    if semana == 10:
        day = 6
        return day
    if semana == 1:
        day = 7
        return day
    else:
        pass

#Agregamos patrones posibles
for i in courses_true.index:
        if courses_true['length'][i] == 22 or courses_true['length'][i] == 10 or  courses_true['length'][i] == 20 :
            try:
                if courses_true['start'][i] == 96 :
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 1)
                elif courses_true['start'][i]  == 108:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 2)
                elif courses_true['start'][i]  == 120:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 3)
                elif courses_true['start'][i]  == 144:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 4)
                elif courses_true['start'][i]  == 156:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 5)
                elif courses_true['start'][i]  == 168:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 6)
                elif courses_true['start'][i]  == 180:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 7)
                elif courses_true['start'][i]  == 192:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 8)
                elif courses_true['start'][i]  == 204:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 9)
                elif courses_true['start'][i]  == 216:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 10)
                elif courses_true['start'][i]  == 228:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 11)
                elif courses_true['start'][i]  == 240:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['days'][i]) * 12)
            except:
                pass
        if courses_true['length'][i] == 34:
            duration34.add(courses_true['class_id'][i])

        if courses_true['length'][i] == 46:
            duration46.add(courses_true['class_id'][i])

        if courses_true['length'][i] == 58:
            duration58.add(courses_true['class_id'][i])
            
        if courses_true['length'][i] == 106:
            duration106.add(courses_true['class_id'][i])

#eliminar keys que estén vacías
for x in duration34:
    del salas_factibles[x]
    del class_limit[x]
    del classes_room[x]
    del patterns[x]
for y in duration46:
    del salas_factibles[y]
    del class_limit[y]
    del classes_room[y]
    del patterns[y]
for z in duration58:
    del salas_factibles[z]
    del class_limit[z]
    del classes_room[z]
    del patterns[z]
for w in duration106:
    del salas_factibles[w]
    del class_limit[w]
    del classes_room[w]
    del patterns[w]

delete_patterns = list()
for i in patterns:
    if patterns[i] == [] or len(patterns[i]) == 1:
        delete_patterns.append(i)
for i in delete_patterns:
    del patterns[i]
delete_all = list()
for  x in class_limit.keys():
    if x not in patterns.keys():
        delete_all.append(x)

for x in delete_all:
    try:
        del class_limit[x]
        del classes_room[x]
        del salas_factibles[x]
    except:
        pass

delete_salas = list()
for x in salas_factibles:
    if len(salas_factibles[x]) <= 1:
        delete_salas.append(x)
for x in delete_salas:
    del salas_factibles[x]
    del classes_room[x]

for x in patterns:
    patterns[x]= set(patterns[x])

same_atendees_conjunto = [[]]
not_overlap_conjunto = [[]]
same_days_conjunto = [[]]
#same_room_conjunto = [[]]
overlap_conjunto = [[]]

