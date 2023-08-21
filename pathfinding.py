import heapq
from types import DynamicClassAttribute

# Definimos las direcciones posibles para moverse en la grid: derecha, izquierda, arriba, abajo.
direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def a_star(grid, inicio, destino):

    def distancia_manhattan(punto1, punto2):
        # Calcula la distancia Manhattan entre dos puntos.
        return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])

    # Tamaño de la grid.
    filas, columnas = grid.__getattribute__("height"), grid.__getattribute__("width")

    # Inicializamos las listas abierta y cerrada.
    lista_abierta = [(0, inicio)]  # Usamos una cola de prioridad para la lista abierta.
    lista_cerrada = set()

    # Inicializamos un diccionario para rastrear los costos.
    g_scores = {inicio: 0}

    # Inicializamos un diccionario para rastrear los padres de cada punto.
    padres = {}

    while lista_abierta:
        _, actual = heapq.heappop(lista_abierta)
         
        if actual in grid.get_neighborhood(destino, moore=False, include_center=False): 
            # Reconstruir el camino si hemos llegado al destino.
            camino = []
            while actual in padres:
                camino.insert(0, actual)
                actual = padres[actual]
            camino.append(destino)
            #     camino.insert(0, inicio) 
            
            return camino

        lista_cerrada.add(actual)

        # for dx, dy in direcciones:
        for vecino in grid.get_neighborhood(actual, moore=False, include_center=False):
            # vecino = actual[0] + dx, actual[1] + DynamicClassAttribute
            # if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas and grid.is_cell_empty(vecino):
            if grid.is_cell_empty(vecino):
                costo_g = g_scores[actual] + 1
                if vecino not in g_scores or costo_g < g_scores[vecino]:
                    g_scores[vecino] = costo_g
                    costo_h = distancia_manhattan(vecino, destino)
                    costo_f = costo_g + costo_h
                    heapq.heappush(lista_abierta, (costo_f, vecino))
                    padres[vecino] = actual

    # Si no se encontró un camino, retornamos una lista vacía.
    return []