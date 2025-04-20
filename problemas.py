#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
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
#  Desarrolla el problema del Camión mágico
# ------------------------------------------------------------

class PblCamionMágico(busquedas.ProblemaBusqueda):
    def __init__(self,n):
       super().__init__(1, lambda estado: estado == n, CamionMagico(n))
       self.n = n

# ------------------------------------------------------------
#  Desarrolla una política admisible.
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
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class CuboRubik(busquedas.ModeloBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def acciones_legales(self, estado):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def sucesor(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

    def costo_local(self, estado, accion):
        raise NotImplementedError('Hay que hacerlo de tarea')

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
    