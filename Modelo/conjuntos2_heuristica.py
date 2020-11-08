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
salas_factibles_heu=dict()
##SALAS FACTIBLES PERO SIN SEPARACIÓN DE clases_salas_factibles = dict()
class_id = courses_room['class_id']
class_id = np.unique(class_id)
count = 0
for x in class_id:

    if x in impares and count < 600:
        salas_factibles[x] = []
        salas_factibles_heu[x] = []
        count += 1
for i in courses_room.index:
    try:
        salas_factibles[courses_room['class_id'][i]].append(courses_room['room_id'][i])
        salas_factibles_heu[courses_room['class_id'][i]].append(courses_room['room_id'][i])
    except:
        pass


## diccionario con key class_id y el value es class_limit 
class_limit = dict()
class_limit_heu=dict()
for x in courses_time.index:
    class_limit[courses_time['class_id'][x]] = courses_time['class_limit'][x]
    class_limit_heu[courses_time['class_id'][x]] = courses_time['class_limit'][x]


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
patterns_heu = dict()
patterns34=dict()
patterns46=dict()
patterns58=dict()
patterns106=dict()
patterns10=dict()
#Rellenamos diccionarios con id de clases con sala

for i in classes_room.keys():
    

    patterns[i] = []
    patterns_heu [i] = []
    penalty_patterns [i] = []
    patterns34 [i] = []
    patterns46[i] = []
    patterns58[i] = []
    patterns106[i] = []
    patterns10[i] = []



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


def days_letra(semana):
    if semana ==  1000000:
        day = 'L'
        return "L"
    if semana == 100000:
        day = 'M'
        return "M"
    if  semana == 10000:
        day = 3
        return "W"
    if semana == 1000:
        day = 4
        return "J"
    if semana == 100:
        day = 5
        return "V"
    if semana == 10:
        day = 6
        return "S"
    if semana == 1:
        day = 7
        return "D"
    else:
        pass





for i in range (1,536):

    patterns106[i] = []
    patterns10[i] = []
    patterns34 [i] = []
    patterns46[i] = []
    patterns58[i] = []
    patterns_heu [i] = []






#Agregamos patrones posibles 
#Además penalidedes de los patrones entrar por curso y obtener [patron, penalidad]
count34 = 0
for i in courses_true.index:
        if courses_true['class_length'][i] == 22  :
            try:
                if courses_true['class_start'][i] == 96 :
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 1)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 1,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 120:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 2)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 2,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                        [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                         courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 144:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 3)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 3,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                        [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                         courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 168:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 4)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 4,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                        [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                         courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 192:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 5)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 5,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                    [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                     courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 216:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 6)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 6,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                        [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                         courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

                elif courses_true['class_start'][i]  == 240:
                    patterns[courses_true['class_id'][i]].append(days_function(courses_true['class_days'][i]) * 7)
                    penalty_patterns[courses_true['class_id'][i]].append([days_function(courses_true['class_days'][i]) * 7,courses_true['class_penalty'][i]])
                    patterns_heu[courses_true['class_id'][i]].append(
                        [days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],
                         courses_true['class_start'][i] + courses_true['class_length'][i] - 1])

            except:
                pass

        #clases no simples se entregan con formato distinto, este se llama por class_id: [día,slot_start,slot_end]

        if courses_true['class_length'][i] == 34:
            try:

                patterns34[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
            except:
                pass
        if courses_true['class_length'][i] == 46:
            try:
                patterns46[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
            except:
                pass
        if courses_true['class_length'][i] == 58:
            try:
                patterns58[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
            except:
                pass
        if courses_true['class_length'][i] == 106:
            ##print([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
            
        
            
            
            
            patterns106[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
    
        if courses_true['class_length'][i] == 10:
            try:
                patterns10[courses_true['class_id'][i]].append([days_letra(courses_true['class_days'][i]),courses_true['class_start'][i],courses_true['class_start'][i]+courses_true['class_length'][i]-1])
            except:
                pass

        # if courses_true['class_length'][i] == 34:
        #     duration34.add(courses_true['class_id'][i])
        #
        # if courses_true['class_length'][i] == 46:
        #     duration46.add(courses_true['class_id'][i])
        #
        # if courses_true['class_length'][i] == 58:
        #     duration58.add(courses_true['class_id'][i])
        #
        # if courses_true['class_length'][i] == 106:
        #     duration106.add(courses_true['class_id'][i])
        # if courses_true['class_length'][i] == 10:
        #     duration10.add(courses_true['class_id'][i])












##################################STUDENTS######################################################
#Hacer diccionarios con estudiantes
#Conjunto ks de cursos que debe tomar el estudiante
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




# #*Heuristica******************************************************************************************************************************
# #**********************************************************************************************************************************************
#Diccionario con las clases que solo contienen un patron factible (creado por Felipe)
one_pattern = dict()
# for i in patterns:
#     if len(patterns[i]) == 1:
#         one_pattern[i]=patterns[i]
for i in patterns:
    if len(patterns[i]) == 1:
        one_pattern[i]=[days_letra(courses_true['class_days'][i]), courses_true['class_start'][i],courses_true['class_start'][i] + courses_true['class_length'][i] - 1]




#Diccionario con las clases que solo contienen una sala factible (creado por Felipe) devuelve los patrones posibles
one_room = dict()
# for i in salas_factibles:
#     if len(salas_factibles_heu[i]) == 1:
#         one_room[i] = salas_factibles_heu[i]

for i in salas_factibles_heu:
    if len(salas_factibles_heu[i]) == 1:
        one_room[i]=[]
        for patron in patterns_heu[i]:#[a,b]+[c,d]=[a,b,c,d]
            one_room[i].append([salas_factibles_heu[i][0]]+patron)
            #one room esta en fommato one_room[1]=[[id_sala, dia, slot_start, slot_end],[id_sala, dia, slot_start, slot_end] ]



#
# #Algoritmo heuristica de asignacion clases con 1 patron factible
##las clases_room es la salas es la key y el value es su capacidad
##rooms de entra por id de la sala y devuelve su capacidad
# for i in one_pattern: #i=12 (la clase 12 solo tiene un patron factible)
#     capacidad_clase=class_limit[i]
#     delta=capacidad_clase
#     room_ok=0
#     for s in salas_factibles[i]: #salas_factibles[12]=[1,4,5] luego s = 1,4,5
#         if ([s, one_pattern[i][0]] not in asignado):
#             if (rooms[s]-capacidad_clase<delta):
#                 delta = rooms[s]-capacidad_clase
#                 room_ok=s
#     if room_ok==0:
#         for s in salas_factibles[i]:  # salas_factibles[12]=[1,4,5] luego s = 1,4,5
#             if ([s, one_pattern[i][0]] not in asignado):
#                 if (rooms[s] - capacidad_clase < capacidad_clase):
#                     room_ok = s
#
#     if room_ok>0:
#         asignado.append([room_ok, one_pattern[i][0]])
#         asignado_con_clase.append([i, room_ok, one_pattern[i][0]])
#     else:
#         cuenta=cuenta+1
#
# print("Asignado")
# for i in asignado:
#      print(i)
# print(len(one_pattern))
# print(len(asignado))
# print(cuenta)


#**********************************************************************************************************************************************
#**********************************************************************************************************************************************
#**********************************************************************************************************************************************
#**************************************************************************************************************************************


# #algoritmo asignación de cursos con 1 sala factible.
# cuenta=0
# for i in one_room: #i=1 (la clase 1 solo tiene la sala 190 factible)
#     pattern_ok = 0
#     for p in patterns[i]: #p tomara todos los patrones de clase i
#         print([one_room[i][0],p] )
#         if ([one_room[i][0],p] not in asignado):
#             pattern_ok = p
#
#
#     if pattern_ok>0:
#         asignado.append([one_room[i][0],pattern_ok])
#         asignado_con_clase.append([i, one_room[i][0], pattern_ok])
#
#     else:
#         cuenta=cuenta+1
#
# print("Asignado")
# for i in asignado:
#      print(i)
# print(len(one_pattern))
# print(len(asignado))
# print(cuenta)




#**********************************************************************************************************************************************
#**************************************************************************************************************************************

#################################DELETE listas vacias########################################################

for i in classes_room.keys():
    if patterns34[i] == []:
        valor=patterns34.pop(i)
    if patterns46[i] == []:
        valor = patterns46.pop(i)
    if patterns58[i] == []:
        valor = patterns58.pop(i)
    if patterns106[i] == []:
        valor = patterns106.pop(i)
    if patterns10[i] == []:
        valor = patterns10.pop(i)
    if patterns_heu[i] == []:
        valor = patterns_heu.pop(i)













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

