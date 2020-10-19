import pandas as pd
import numpy as np
import xlrd
import math
#importar salas
room = pd.read_excel('iku-fal17/room.xls')
#todos los cursos
#Keys(course_id, config_id, subpart_id, class_id, class_limit, class_room, class_parent, days, 
# start, length, weeks, penalty)
courses_time = pd.read_csv('iku-fal17/cursos_tiempo.csv',delimiter=';')
#cursos con salas
courses_room = pd.read_csv('iku-fal17/cursos_room.csv',delimiter=';')
#cursos con restricciones de distribución
distribucion = pd.read_csv('iku-fal17/distribucion.csv',delimiter=',')
#### conjuntos listos 
rooms = dict()
#creeación de conjunto de salas
for x in room.index:  
    rooms[room['id '][x]] = room['capacity'][x]

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

modulos = [x for x in range(1,7)]
print(modulos)





