import pandas as pd
import numpy as np
import xlrd
#Parametros
#Cantidad de cursos
m = 62
#Cantidad de clases
c = 100

##se leen los archivos y se crean los conjuntos como arreglos (listas de listas)
room = pd.read_excel('room.xls')
#Arreglar columna days con 0 
room.loc[room['days'] == 100, 'day'] = "0000100"
room.loc[room['days'] == 1000, 'day'] = "0001000"
room.loc[room['days'] == 10000, 'day'] = "0010000"
room.loc[room['days'] == 100000, 'day'] = "0100000"
room.loc[room['days'] == 1000000, 'day'] = "1000000"
#Aqui se borro la columna days y se cambio por day
room = room.drop(['days'], axis=1)
#Conjunto de id de salas con su capacidad
room_id_cap = room.values[:, [True, True, False, False, False, False]]
room_id_cap = np.unique(room_id_cap)

#Conjunto de Salas con toda la informacion
rooms = room.to_numpy()

#Cursos 
course = pd.read_excel('course.xls')
#conjunto de toda la informacion de los cursos
courses = course.to_numpy()

#Conjunto de cursos que no necesitan sala
courses_false = course[course.class_room == False]
courses_false = courses_false.drop(['room_id','room_penalty'], axis=1)
courses_true = course[(course['class_room'] != False)]
courses_true = courses_true.drop(['class_room'], axis = 1)

#Arreglo de los cursos que no necesitan sala
courses_false = courses_false.to_numpy()

#Abrir cursos_room
courses_room = pd.read_excel('cursos_room.xls')

#Salas factibles para una clase c en diccionarios de la forma {1: [2,3,4]}
salas_factibles = dict()
class_limit = dict()

class_id = courses_room['class_id']

class_id = np.unique(class_id)
for x in class_id:
    salas_factibles[x] = []
    class_limit[x]= []
    
for i in courses_room.index:
    salas_factibles[courses_room['class_id'][i]].append(courses_room['room_id'][i])
    class_limit[courses_room['class_id'][i]].append(courses_room['class_limit'][i])  
#Todas las salas factibles para un curso estan disponibles en 
#salas_factibles que es un diccionario

print(class_limit)
#capacidad de cada clase



horario = course[course.course_id == 4]





#Restricciones de Distribucion
distribution = pd.read_excel('distribucion.xls') 
distributions = distribution.to_numpy()





#Estudiantes los ocuparemos en segunda etapa
#student = pd.read_excel('student_0.xls') 
#students = student.to_numpy()
#Restricciones de Distribucion