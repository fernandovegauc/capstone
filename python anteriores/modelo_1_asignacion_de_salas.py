from gurobipy import *
import numpy as np
m=Model("mip1")
D=range(2,7)
for i in D:
    print(i)
SO=range(2)
Sd=range(58)
S=range(20)
S1=range(2)
S2=range(2)
Rc=range(2)
Sc=range(4)
R=range(20)
C=range(10)
M=range(8)
lecM=range(6)
A=range(10)
V=range(20)
Vc=range(2)
initc=range(2)
slot=range(10)
sdnvc=range(3)
xvars=[]
xsvars=[]
yvars=[]
yrvars=[]
for a in C:
    lc=[]
    for c in A:
        x_a_c=m.addVar(obj=0, vtype=GRB.BINARY,name="xa"+str(a)+"c"+str(c))
        lc.append(x_a_c)
    xvars.append(lc)
for a in C:
    lc=[]
    for c in A:
        ls=[]
        for s in S:
            xs_a_c_s=m.addVar(obj=0, vtype=GRB.BINARY,name="xsa"+str(a)+"c"+str(c)+"s"+str(s))
            ls.append(xs_a_c_s)
        lc.append(ls)
    xsvars.append(lc)
for c in C:
    lc = []
    for v in V:
        lv=[]
        for s in S:
            y_c_v_s = m.addVar(obj=0, vtype=GRB.BINARY, name="yc" + str(c) + "v" + str(v) + "s" + str(s))
            lv.append(y_c_v_s)
        lc.append(lv)
    yvars.append(lc)
for c in C:
    lc = []
    for r in R:
        lr=[]
        for s in S:
            yr_c_r_s = m.addVar(obj=0, vtype=GRB.BINARY, name="yrc" + str(c) + "r" + str(r) + "s" + str(s))
            lr.append(yr_c_r_s)
        lc.append(lr)
    yrvars.append(lc)
m.update()
m.setObjective(GRB.MINIMIZE)

#tambien se puede setear el objetivo como m.setObjective(ACA VA LA F.O. que sera enorme, GRB.MINIMIZE)
#restriccion 1

#restriccion 3: programar eventos de una clase en exactamente un bloque horario entre los factibles
for c in C:
    for v in Vc:
        m.addConstr(quicksum(yvars[c][v][s] for s in SO) == 1)#es un Sc en realidad
#restriccion 4: Asignar la frecuencia semanal.
#v=1 #aca se asume que v=1 es un modulo con codigo 1, pero depende de cada c
#for d in D:
    #for c in C:
        #m.addConstr(quicksum(yvars[c][v][s] for s in S) <= 1)
#restriccion 5: Los eventos de un mismo dia son consecutivo
for d in D:
    for c in C:
        for so in SO:
            for so in sdnvc:
                for vi in initc:
                    nvc=5
                    #nvc=dict....aqui se debe reconocer el parametro nvc
                    m.addConstr(quicksum(yvars[c][v][s] for v in range(vi+1,vi+nvc) for s in range(so+1,so+nvc)) -(nvc-1)*yvars[c][vi][so] == 0)
#




#restriccion 7: No tener superposicion horaria para las salas, un curso en la sala en ese bloque
for r in R:
    for s in S:
        m.addConstr(quicksum(yrvars[c][r][s] for c in C for r in R) <= 1)
#restriccion 8: Asignar sala a una clase en un bloque horario determinada
for c in C:
    for s in S:
        m.addConstr((quicksum(yrvars[c][r][s] for r in R)) == (quicksum(yvars[c][v][s] for v in V)))
#resgtriccion 9: No hay cambio de sala dentro de un mismo dia


for c in C:
    for so in SO:
        for so in sdnvc:
            for vi in initc:
                for r in Rc:
                    nvc=5
                    #nvc=dict....aqui se debe reconocer el parametro nvc
                    m.addConstr(quicksum(yvars[c][r][s] for s in range(so+1,so+nvc))>=(nvc-1)*(yvars[c][vi][so]+yrvars[c][r][so]-1))
#

#restriccion 10: No tener tope de horario entre las clases asignados al alumno
# for a in A:
#     for s in S:
#         m.addConstr(quicksum(xsvars[a][c][s] for c in C for m in M) <= 1)
#restriccion 11: relacionar variables
# for c in C:
#     for v in V:
#         for s in S:
#             for a in A:
#                 #for m M: tenemos que activarlo cuando hagamos bien los subconjuntos
#                     m.addConstr(yvars[c][v][s]+xvars[a][c]-xsvars[a][c][s] <= 1)
#
# #restriccion 12: relacionar variables
# for a in A:
#     for c in C:
#         for s in S:
#             #for m in M:tenemos que activarlo cuando hagamos bien los subconjuntos
#             m.addConstr(2*xsvars[a][c][s]-(quicksum(yvars[c][v][s] for v in V)-xvars[a][c])<=0)

m.optimize()
print("e")
# for c in C:
#     for v in V:
#         for s in S:
#             if yvars[c][v][s]==1:
#                 print(yvars[c][v][s])
print(xvars)