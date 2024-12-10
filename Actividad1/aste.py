import pygame
from queue import PriorityQueue
from math import sqrt

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        self.color = PURPURA

    def hacer_visitado(self):
        self.color = ROJO

    def hacer_explorado(self):
        self.color = VERDE

    def restablecer(self):
        self.color = BLANCO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        direcciones = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Movimiento cardinal
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Movimiento diagonal
        ]
        for df, dc in direcciones:
            nueva_fila, nueva_col = self.fila + df, self.col + dc
            if 0 <= nueva_fila < self.total_filas and 0 <= nueva_col < self.total_filas:
                vecino = grid[nueva_fila][nueva_col]
                if not vecino.es_pared():
                    self.vecinos.append((vecino, sqrt(2) if df != 0 and dc != 0 else 1))

def heuristica(p1, p2):
    # Distancia Manhattan
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_camino(came_from, nodo_actual, dibujar):
    while nodo_actual in came_from:
        nodo_actual = came_from[nodo_actual]
        nodo_actual.hacer_camino()
        dibujar()

def algoritmo_a_star(dibujar, grid, inicio, fin):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, inicio))
    came_from = {}

    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[inicio] = 0

    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[inicio] = heuristica(inicio.get_pos(), fin.get_pos())

    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        nodo_actual = open_set.get()[2]
        open_set_hash.remove(nodo_actual)

        if nodo_actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            return True

        for vecino, costo in nodo_actual.vecinos:
            temp_g_score = g_score[nodo_actual] + costo

            if temp_g_score < g_score[vecino]:
                came_from[vecino] = nodo_actual
                g_score[vecino] = temp_g_score
                f_score[vecino] = temp_g_score + heuristica(vecino.get_pos(), fin.get_pos())

                if vecino not in open_set_hash:
                    count += 1
                    open_set.put((f_score[vecino], count, vecino))
                    open_set_hash.add(vecino)
                    vecino.hacer_explorado()

        dibujar()

        if nodo_actual != inicio:
            nodo_actual.hacer_visitado()

    return False

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    FILAS = 10  # Ajustado a 19x19
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    algoritmo_a_star(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)