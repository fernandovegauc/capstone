import pandas as pd
import numpy as np
import xlrd
import math

#Parametros
#Cantidad de cursos
m = 62
#Cantidad de clases
c = 100
#Conjunto dias de semana
S = ['L', 'M', 'W', 'J','V','S','D', 'X']

#Cargar Bases de datos
#Base Salas keys(id,capacity)
room = pd.read_excel('iku-fal17/room.xls')
#*******Arreglo de las salas con su id y capacidad*******
rooms = room.to_numpy()

#Bases du
#Cursos_tiempo ****Tiene TODOS los cursos con todas las posibles combinaciones de horario****
#Keys(course_id, config_id, subpart_id, class_id, class_limit, class_room, class_parent, days, 
# start length, weeks, penalty)
courses_time = pd.read_csv('iku-fal17/cursos_tiempo.csv',delimiter=';')
#courses_time = courses_time.drop(['Unnamed: 12','Unnamed: 13'], axis = 1)

#Array de TODA la informacion de los cursos por disponibilidad
courses = courses_time.to_numpy()

#**********Conjunto de cursos que no necesitan sala***********
courses_false = courses_time[courses_time.class_room == False]
courses_false = courses_false.to_numpy()
#**********Conjunto de cursos que si necesitan sala***********
#Keys(course_id, config_id, subpart_id, class_id, class_limit, class_parent, days, 
# start length, weeks, penalty)
courses_true = courses_time[(courses_time['class_room'] != False)]
courses_true = courses_true.drop(['class_room'], axis = 1)
courses_true = courses_true.to_numpy()

#Bases Cursos
#Cursos_room ****Tiene TODOS los cursos que SI requieren sala sin su disponibilidad****
#Keys (courses_id, config_id, subpart_id, class_id, class_limit, class_parent, room_id, room_penalty)
courses_room = pd.read_csv('iku-fal17/cursos_room.csv',delimiter=';')

distribucion = pd.read_csv('iku-fal17/distribucion.csv',delimiter=',')

same_atendees_conjunto = [[]]
not_overlap_conjunto = [[]]
same_days_conjunto = [[]]
count_atendees = 0
count_notoverlap = 0
count_samedays = 0
for i in distribucion.index :
    if i  < len(distribucion.index) - 1:
        if distribucion['type'][i] == 'SameAttendees':
            same_atendees_conjunto[count_atendees].append(distribucion['class_id'][i])
        if distribucion['type'][i] == 'NotOverlap':
            
            not_overlap_conjunto[count_notoverlap].append(distribucion['class_id'][i])
        if distribucion['type'][i] == 'SameDays':
            
            same_days_conjunto[count_samedays].append(distribucion['class_id'][i])
            

        if distribucion['class_id'][i] > distribucion['class_id'][i + 1] : 
            #same_atendees_conjunto[count].append(same_atendees['class_id'][i + 1])
            
            if distribucion['type'][i] == 'SameAttendees':
             
                same_atendees_conjunto.append([])
                count_atendees += 1
            if distribucion['type'][i] == 'NotOverlap':
                
             
                not_overlap_conjunto.append([])
                count_notoverlap += 1
            if distribucion['type'][i] == 'SameDays':
            
            
                same_days_conjunto.append([])
                count_samedays += 1



     
    
            
        

#******************Aqui inicia la separacion de conjuntos*********************

#Salas factibles para una clase c en diccionarios de la forma {1: [2,3,4]}
#Salas_ factibles es un diccionario con una lsita de todas las salas disponibles para un curso
#class_limit es el limite de las clases
#config configuración del Curso m perteneciente a M Q^m (en español tenemos el dic con la config y el id class)

salas_factibles = dict()
class_limit = dict()
config = dict()

class_id = courses_room['class_id']
class_id = np.unique(class_id)

for x in class_id:
    salas_factibles[x] = []
    class_limit[x]= set()

for i in courses_room.index:
    salas_factibles[courses_room['class_id'][i]].append(courses_room['room_id'][i])
    class_limit[courses_room['class_id'][i]].add(courses_room['class_limit'][i]) 

#### Aquí queremos crear config
class_config = courses_time['config_id']
class_config = np.unique(class_config)

for x in class_config:
    config[x] = set()
for i in courses_time.index:
    config[courses_time['config_id'][i]].add(courses_time['class_id'][i])

#Vamos a trabajar con bloques de 6 slots parte 108 y termina en 252
##acá definimos los bloques del día (spn 24 bloques de 6 slots cada 1)

bloques = dict()
count = 0
for i in range(1,25):
    bloques[i] = [108 + 6 * count , 114 + 6 * count]
    count += 1

#acá se define el subconjunto de los bloques para cada clase 
bloques_clase = dict()
duracion_clase = dict()
primeros_bloques = dict()
conjunto_V =dict()
conjunto_Vc=dict()

#Poblar
c_id = courses_time['class_id']
c_id = np.unique(c_id)
for x in c_id:
    bloques_clase[x] = []     #M este es el conjunto Vc
    duracion_clase[x] = []
    primeros_bloques[x] = []

#*****FUNCIONES********
def calcular(inicio,final, bloques):
    rangos = []
    b1=0
    for x in range(1,25):
        if inicio in range(bloques[x][0],bloques[x][1]):
            b1 = x        
    rangos.append(b1)
    return rangos


def days_function(semana):
    if semana ==  1000000:
        day = 'L'
        return day
    if semana == 100000:
        day = 'M'
        return day
    if  semana == 10000:
        day = 'W'
        return day
    if semana == 1000:
        day = 'J'
        return day
    if semana == 100:
        day = 'V'
        return day
    if semana == 10:
        day = 'S'
        return day
    if semana == 1:
        day = "D"
        return day
    else:
        return "X"

for i in courses_time.index:
    
    inicio = courses_time['start'][i]
    final = courses_time['length'][i] + inicio
    rangos = calcular(inicio, final, bloques)
    duracion = math.ceil(courses_time['length'][i]/6)
    day = days_function(courses_time['days'][i])
   
    primeros_bloques[courses_time['class_id'][i]].append([day, calcular(inicio, final, bloques)])
   
    count = 0
    while len(rangos) != duracion: 
        rangos.append(rangos[count] + 1)
        count += 1

    bloques_clase[courses_time['class_id'][i]].append([day,rangos])

# Conjunto duracion clase
for i in bloques_clase:
    for x in bloques_clase[i]:
        duracion_clase[i] = len(x[1]) 

#conjunto_v lista con cuantos eventos teine una clase
for i in duracion_clase:
    conjunto_V[i] = list(range(duracion_clase[i]))

#conjuntos_vc 
#for i in bloques_clase:
#    print(bloques_clase[i])
#    for x in bloques_clase[i]:

#print(primeros_bloques)
#print(primeros_bloques)



