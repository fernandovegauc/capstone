import pandas as pd
import numpy as np
import xlrd
import math

#importar salas
room = pd.read_csv('muni-fi-fal-17/room_capacity.csv',delimiter=';')

#importar cursos
#cursos tiempo
#courses_time = pd.read_csv('muni-fi-fal-17/cursos_tiempo.txt',delimiter=';')
courses_time = pd.read_csv ('muni-fi-fal-17/cursos_tiempo.csv',delimiter=',')
##courses_time = courses_time.to_csv ('muni-fi-fal-17/cursos_tiempo.csv', index=None)

#cursos con salas
courses_room = pd.read_csv('muni-fi-fal-17/curso_sala.csv',delimiter=',')


#cursos con restricciones de distribución
distribucion = pd.read_csv('muni-fi-fal-17/rest_dist.csv',delimiter=';')

#estudiantes
estudiantes = pd.read_csv('muni-fi-fal-17/estudiantes.csv',delimiter=';')



#### conjuntos listos 
rooms = dict()
#creeación de conjunto de salas
#check
for x in room.index:  
    rooms[room['id '][x]] = room['capacity'][x]



####Dividir cursos por semanas
pares = set()
clases_pares = courses_time[(courses_time['class_weeks'] == 111111111111)  ] 
for x in clases_pares.index:
    pares.add(clases_pares['class_id'][x])


impares = set()

clases_impares = courses_time[ (courses_time['class_weeks'] == 1111111111111) ]
for x in clases_impares.index:
    impares.add(clases_impares['class_id'][x])


##creamos las salas factibles para cada clase
salas_factibles = dict()
## Creamos el diccionario que contiene las penalidades de escoger una sala
###Key: Id clase ; Values: [sala, penalidad]
penalty_room=dict()
##SALAS FACTIBLES PERO SIN SEPARACIÓN DE clases_salas_factibles = dict()
class_id = courses_room['class_id']
class_id = np.unique(class_id)
count = 0
for x in class_id:
    penalty_room[x] = {}
    if x in impares and count < 600:
        salas_factibles[x] = []
        count += 1
for i in courses_room.index:
    try:
        salas_factibles[courses_room['class_id'][i]].append(courses_room['room_id'][i])
    except:
        pass
for i in courses_room.index:
    try:
        penalty_room[courses_room['class_id'][i]][courses_room['room_id'][i]] = courses_room['room_penalty'][i] 
    except:
        pass

## diccionario con key class_id y el value es class_limit 
class_limit = dict()
for x in courses_time.index:
    class_limit[courses_time['class_id'][x]] = courses_time['class_limit'][x]



##las keys son los courses_id y por el momento el value es una lista vacía
### hay que agregarle las clases 
courses = dict()
course_id = courses_room['course_id']
course_id = np.unique(course_id)
for x in course_id:
    courses[x] = set()
for x in courses_time.index:
    courses[courses_time['course_id'][x]].add(courses_time['class_id'][x])


##las clases que requieren salas es la key y el value es su capacidad
courses_true = courses_time[(courses_time['class_room']!=False)]
courses_true = courses_true.drop(['class_room'], axis = 1)
classes_room = dict()
#print(class_id)
count = 0
for x in class_id:
 
    if x in impares and count < 600:

        classes_room[x] = set()
        count += 1
for x in courses_true.index:
   
    try:
        classes_room[courses_true['class_id'][x]].add(courses_true['class_limit'][x])
    except:
        pass

#print(classes_room)

## las clases que no requieren salas, salas es la key y el value es su capacidad
courses_false = courses_time[(courses_time['class_room'] == False)]
courses_false = courses_false.drop(['class_room'], axis = 1)
classes_no_room = dict()
for x in courses_false.index:
    classes_no_room[courses_false['class_id'][x]] = courses_false['class_limit'][x]


##modulos horarios van del 1 al 6 parten en el 108 y terminan en en 252
modulos = dict()
count = 0
for i in range(1,7):
    modulos[i] = [96 + 24 * count , 108 + 24 * count]
    count += 1


## Cursos cacho con duracion 34 y 46, se hacen dos set
duration34 = set()
duration46 = set()
duration58 = set()
duration106 = set()
duration10 = set()
##conjunto de patrones factibles para la clase c que tiene SALA
patterns = dict()
penalty_patterns = dict()
#Rellenamos diccionarios con id de clases con sala
for i in classes_room.keys():
    patterns[i] = []
    penalty_patterns [i] = {}


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
#Además penalidedes de los patrones entrar por curso y obtener [patron, penalidad]
for i in courses_true.index:
        if courses_true['class_length'][i] == 22  :
            try:
                if courses_true['class_start'][i] == 96 :
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 1)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i])*1] = courses_true['class_penalty'][i]
               
                elif courses_true['class_start'][i]  == 120:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 2)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 2] =courses_true['class_penalty'][i]
                elif courses_true['class_start'][i]  == 144:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 3)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 3] =courses_true['class_penalty'][i]
                
                elif courses_true['class_start'][i]  == 168:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 4)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 4] =courses_true['class_penalty'][i]
                
                elif courses_true['class_start'][i]  == 192:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 5)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 5] =courses_true['class_penalty'][i]
                
                elif courses_true['class_start'][i]  == 216:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 6)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 6] =courses_true['class_penalty'][i]
                elif courses_true['class_start'][i]  == 240:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 7)
                    penalty_patterns[courses_true['class_id'][i]][days_function(courses_true['class_days'][i]) * 7] =courses_true['class_penalty'][i]
            except:
                pass
        if courses_true['class_length'][i] == 34:
            duration34.add(courses_true['class_id'][i])

        if courses_true['class_length'][i] == 46:
            duration46.add(courses_true['class_id'][i])

        if courses_true['class_length'][i] == 58:
            duration58.add(courses_true['class_id'][i])
            
        if courses_true['class_length'][i] == 106:
            duration106.add(courses_true['class_id'][i])
        if courses_true['class_length'][i] == 10:
            duration10.add(courses_true['class_id'][i])

# diccionario de clases y sus padres key class_id value parent_id 
df_clean= courses_time[courses_time.class_parent.notnull()]
parent = dict()
for i in df_clean.index:
    parent[df_clean['class_id'][i]] =int(df_clean['class_parent'][i])


##################################STUDENTS######################################################
#Hacer diccionarios con estudiantes
#Conjunto ks de cursos que debe tomar el estudiante
#llave del diccionario id de estudiante, valores son los id de los cursos.
students = dict()
for x in estudiantes['student_id']:
    students[x] = set()
for x in estudiantes.index:
    students[estudiantes['student_id'][x]].add(estudiantes['course_id'][x])
#Zw conjunto de subpartes de la configuración -> se modifico a course_id y subparte respectiva porque 
#todos los cursos solo tienen una configuración (EXCEPTO EL 37)
zw = dict()
for x in course_id:
    zw[x] = set()
for y in courses_time.index:
    zw[courses_time['course_id'][y]].add(courses_time['subpart_id'][y])
#Cl conjunto de clases de la subparte
cl= dict()
for x in courses_time['subpart_id']:
    cl[x] = set()
for y in courses_time.index:
    cl[courses_time['subpart_id'][y]].add(courses_time['class_id'][y])
#Sk conjunto de estudiantes que deben asistir al curso k
sk = dict()
for x in course_id:
    sk[x] = set()

for x in students.keys():
     for y in course_id:
        if y in students[x]:
             sk[y].add(x)



#################################DELETE########################################################
#Filtrar por clases que NO pueden tomar los estudiantes

#eliminar keys que estén vacías
for x in duration34:
    try:
        del salas_factibles[x]
        del class_limit[x]
        del classes_room[x]
        del patterns[x]
    except:
        pass

for y in duration46:
    try:
        del salas_factibles[y]
        del class_limit[y]
        del classes_room[y]
        del patterns[y]
    except:
        pass
for y in duration58:
    try:
        del salas_factibles[y]
        del class_limit[y]
        del classes_room[y]
        del patterns[y]
    except:
        pass
for y in duration106:
    try:
        del salas_factibles[y]
        del class_limit[y]
        del classes_room[y]
        del patterns[y]
    except:
        pass

for y in duration10:
    try:
        del salas_factibles[y]
        del class_limit[y]
        del classes_room[y]
        del patterns[y]
    except:
        pass




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
    if len(salas_factibles[x]) <= 3:
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


class_limit_s = dict()
for x in courses_time.index:
    class_limit_s[courses_time['class_id'][x]] = courses_time['class_limit'][x]

#################################PENALIDADES##################################################
room_penalty = dict()
for x in courses_room['class_id']:
    room_penalty[x] = []
for x in courses_room.index:
    room_penalty[courses_room['class_id'][x]].append([courses_room['room_id'][x],courses_room['room_penalty'][x]])
