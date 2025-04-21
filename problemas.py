#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas



# ------------------------------------------------------------
#  Modelo del Camión mágico
# ------------------------------------------------------------

class CamionMagico(busquedas.ModeloBusqueda):
    def __init__(self,n):
        self.n = n

    def acciones_legales(self, estado):
        acciones=[]

        if estado + 1 <= self.n: 
            acciones.append("caminar")
        if 2 * estado <= self.n: 
            acciones.append("camion")
        return acciones

    def sucesor(self, estado, accion):
        if accion == 'caminar':
            return estado + 1
        elif accion == 'camion':
            return 2 * estado
        else:
            raise ValueError("Accion inválida, es caminar o camión")

    def costo_local(self, estado, accion):
        if accion == 'caminar':
            return 1
        elif accion == 'camion':
            return 2
        else:
            raise ValueError("Accion inválida")

    @staticmethod
    def bonito(estado):
        return f"Estado: {estado}"
 
# ------------------------------------------------------------
#  Problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    def __init__(self,n):
       super().__init__(1, lambda estado: estado == n, CamionMagico(n))
       self.n = n

# ------------------------------------------------------------
#  Políticas admisibles: 
# ------------------------------------------------------------
# ------------------------------------------------------------
#   1 Tennis
#   Heurística; El único movimiento posible es caminar(costo 1) 
#   Justificación: Nunca va a ser mayor que el costo real porque en el 
#   peor de los casos solo se puede caminar y como el camion(costo 2) cuesta más ,
#   caminar siempre sera el minimo costo posible
#   °Es admisible por que no sobreestima el costo real
#   °Es simple
#    Para llamarla = h_1_camion_magico(nodo, problema.n) porque tuve problemas
#    con el problema.n 
#  ------------------------------------------------------------

def h_1_camion_magico(nodo,meta):
    return max(0,meta - nodo.estado)

# ------------------------------------------------------------
#   2 Llantas
#   Heurística; Usar lo más posible el camión
#   Justificación: Como se prefiere utilizar el camión el estado actual va a ir duplicandose
#   hasta que se acerque lo suficiente a la menta y ya no pueda utilizarse el camión, se caminara
#   recordando que el cosrto del caminón (2) y el de caminar(1) el costo será una estimación de estos dos
#   °Es admisible porque no sobreestima el costo real
#   °Explora menos nodos
#  ------------------------------------------------------------

def h_2_camion_magico(nodo):
    actual = nodo.estado
    meta = nodo.problema.n if hasattr(nodo, "problema") else 20 

    if actual >= meta:
        return 0

    km= 0
    pos = actual
    while pos * 2 <= meta:
        pos *= 2
        km += 1

    falta = max(0, meta - pos)
    return km * 2 + falta

# ------------------------------------------------------------
#  Modelo Cubo Rubik
# ------------------------------------------------------------
# ------------------------------------------------------------
#   Un cubo Rubik tiene 6 caras donde cada cara tiene 9 cuadrados del mismo color
#   1 blanco(b), 2 rojo(r), 3 verde(v), 4 naranja(n),  5 azul(a) y 6 amarillo(m)
#         ┌───────┐
#         │ r r r │
#         │ r r r │
#         │ r r r │
# ┌───────┬───────┬───────┬───────┐
# │ b b b │ v v v │ a a a │ m m m │
# │ b b b │ v v v │ a a a │ m m m │
# │ b b b │ v v v │ a a a │ m m m │
# └───────┴───────┴───────┴───────┘
#         │ n n n │
#         │ n n n │
#         │ n n n │
#         └───────┘
#   
#             ┌──────────┐
#             │ r0 r1 r2 │
#             │ r3 r4 r5 │
#             │ r6 r7 r8 │
# ┌──────────┬──────────┬──────────┬──────────┐
# │ b0 b1 b2 │ v0 v1 v2 │ a0 a1 a2 │ m0 m1 m2 │
# │ b3 b4 b5 │ v3 v4 v5 │ a3 a4 a5 │ m3 m4 m5 │
# │ b6 b7 b8 │ v6 v7 v8 │ a6 a7 a8 │ m6 m7 m8 │
# └──────────┴──────────┴──────────┴──────────┘
#            │ n0 n1 n2 │
#            │ n3 n4 n5 │
#            │ n6 n7 n8 │
#            └──────────┘
#   Cuadrado de cada cara: normal
#         ┌───────┐
#         │ 0 1 2 │
#         │ 3 4 5 │
#         │ 6 7 8 │
#         └───────┘
#   Cuadrado de cada cara: un giro a la izquierda
#         ┌───────┐
#         │ 6 3 0 │
#         │ 7 4 1 │
#         │ 8 5 2 │
#         └───────┘
#   Cuadrado de cada cara: un giro a la derecha
#         ┌───────┐
#         │ 2 5 8 │
#         │ 1 4 7 │
#         │ 0 3 6 │
#         └───────┘
#  ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    def __init__(self,estado_inicial):
        self.estado = estado_inicial

    def acciones_legales(self, estado):
        # Donde < es giro a la izquierda/horario
        # y > es giro a la derecha/ antihorario
        return ['<B','B>','<R','R>','<V','V>','<N','N>','<A','A>','<M','M>',]

    def giro_izq(c):
        return [c[6], c[3], c[0],
                c[7], c[4], c[1],
                c[8], c[5], c[2]]
    def giro_der(c):
        return [c[2], c[5], c[8],                   
                c[1], c[4], c[7],
                c[0], c[3], c[6]]    
        
    def sucesor(self, estado, accion):
        nuevo = {c: estado[c].copy() for c in estado}
        c = accion[1]

        if c == '<V':
# giro <V:
#             ┌──────────┐
#             │ r0 r1 r2 │
#             │ r3 r4 r5 │
#             │ b8 b5 b2 │
# ┌──────────┬──────────┬──────────┬──────────┐
# │ b0 b1 n0 │ v0 v1 v2 │ r6 a1 a2 │ m0 m1 m2 │
# │ b3 b4 n1 │ v3 v4 v5 │ r7 a4 a5 │ m3 m4 m5 │
# │ b6 b7 n2 │ v6 v7 v8 │ r8 a7 a8 │ m6 m7 m8 │
# └──────────┴──────────┴──────────┴──────────┘
#            │ a6 a3 a0 │
#            │ n3 n4 n5 │
#            │ n6 n7 n8 │
#            └──────────┘
            nuevo[c] = self.giro_izq(estado[c])
            temp= estado['R'][6:9]
            nuevo['R'][6:9]=estado['B'][8:1:-3] # tambien puede ser [2::3][::-1]
            nuevo['B'][2::3]=estado['N'][0:3]
            nuevo['N'][0:3]=estado['A'][0::3]
            nuevo['A'][0::3]=temp


        elif c == 'V>':
# giro V>:
#             ┌──────────┐
#             │ r0 r1 r2 │
#             │ r3 r4 r5 │
#             │ a0 a3 a6 │
# ┌──────────┬──────────┬──────────┬──────────┐
# │ b0 b1 r8 │ v0 v1 v2 │ n2 a1 a2 │ m0 m1 m2 │
# │ b3 b4 r7 │ v3 v4 v5 │ n1 a4 a5 │ m3 m4 m5 │
# │ b6 b7 r6 │ v6 v7 v8 │ n0 a7 a8 │ m6 m7 m8 │
# └──────────┴──────────┴──────────┴──────────┘
#            │ b2 b5 b8 │
#            │ n3 n4 n5 │
#            │ n6 n7 n8 │
#            └──────────┘
            nuevo[c] = self.giro_der(estado[c])
            temp= estado['R'][6:9]
            nuevo['R'][6:9]=estado['A'][0::3]
            nuevo['A'][0::3]=estado['N'][0:3][::-1]
            nuevo['N'][0:3]=estado['B'][2::3]
            nuevo['B'][2::3]=temp [::-1]

        elif c == '<B':
#    giro <B:
#             ┌──────────┐
#             │ r2 r5 r8 │
#             │ r1 r4 r7 │
#             │ m8 m5 m2 │
# ┌──────────┬──────────┬──────────┬──────────┐
# │ m0 m1 n6 │ b0 b1 b2 │ r0 v1 v2 │ a0 a1 a2 │
# │ m3 m4 n3 │ b3 b4 b5 │ r3 v4 v5 │ a3 a4 a5 │
# │ m6 m7 n0 │ b6 b7 b8 │ r6 v7 v8 │ a6 a7 a8 │
# └──────────┴──────────┴──────────┴──────────┘
#            │ v6 v3 v0 │
#            │ n7 n4 n1 │
#            │ n8 n5 n2 │
#            └──────────┘
            nuevo[c] = self.giro_izq(estado[c])
            temp= estado['R'][0::3]
            nuevo['R'][0::3]=estado['M'][2::3][::-1]
            nuevo['M'][2::3]=estado['N'][0::3][::-1]
            nuevo['N'][0::3][::-1]=estado['V'][0::3][::-1]
            nuevo['V'][0::3]=temp

        elif c == 'B>':
# giro B>:
#             ┌──────────┐
#             │ r2 r5 r8 │
#             │ r1 r4 r7 │
#             │ v0 v3 v6 │
# ┌──────────┬──────────┬──────────┬──────────┐
# │ m0 m1 r6 │ b0 b1 b2 │ n0 v1 v2 │ a0 a1 a2 │
# │ m3 m4 r3 │ b3 b4 b5 │ n3 v4 v5 │ a3 a4 a5 │
# │ m6 m7 r0 │ b6 b7 b8 │ n6 v7 v8 │ a6 a7 a8 │
# └──────────┴──────────┴──────────┴──────────┘
#            │ m2 m5 m8 │
#            │ n7 n4 n1 │
#            │ n8 n5 n2 │
#            └──────────┘
            nuevo[c] = self.giro_der(estado[c])
            temp= estado['R'][0::3]
            nuevo['R'][6:9]=estado['V'][0::3]
            nuevo['V'][0::3]=estado['N'][0:3]
            nuevo['N'][0::3][::-1]=estado['B'][2::3]
            nuevo['M'][2::3]=temp [::-1]

    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        raise NotImplementedError('Hay que hacerlo de tarea')
 
 # ------------------------------------------------------------
#  Desarrolla el problema del Cubo de Rubik
# ------------------------------------------------------------

class PblCuboRubik(busquedas.ProblemaBusqueda):
    """
    El problema a resolver es establecer un plan para resolver el cubo de rubik.

    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0



def compara_metodos(problema, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n\n')


if __name__ == "__main__":


    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    problema = PblCamionMágico( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    problema = PblCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    