

# Visualización de Nodos con Algoritmo A*

## Descripción
Este código implementa una visualización del algoritmo A* utilizando la biblioteca `pygame` para la interfaz gráfica. El programa permite al usuario interactuar con una cuadrícula, seleccionar un nodo inicial y final, y dibujar paredes para simular obstáculos. El algoritmo A* encuentra el camino más corto desde el nodo inicial al nodo final, y este se visualiza en la cuadrícula.

## Importaciones y Configuraciones Iniciales

```python
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
```

### Importaciones
- **pygame**: Biblioteca utilizada para la creación de videojuegos y visualizaciones gráficas.
- **PriorityQueue**: Clase de la biblioteca `queue` que implementa una cola de prioridad, esencial para el algoritmo A*.
- **sqrt**: Función de la biblioteca `math` que calcula la raíz cuadrada, utilizada para las distancias diagonales.

### Configuraciones Iniciales
- **ANCHO_VENTANA**: Define el ancho y la altura de la ventana de visualización en píxeles.
- **VENTANA**: Inicializa una ventana de `pygame` con las dimensiones especificadas por `ANCHO_VENTANA`.
- **pygame.display.set_caption**: Establece el título de la ventana de `pygame`.

### Colores (RGB)
- **BLANCO, NEGRO, GRIS, VERDE, ROJO, NARANJA, PURPURA**: Definiciones de colores en formato RGB, utilizados para representar diferentes estados de los nodos en la visualización (por ejemplo, nodos de inicio, fin, paredes, camino, explorados, visitados).


## Clase Nodo

```python
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
```


La clase `Nodo` es fundamental para representar cada celda de la cuadrícula en la visualización del algoritmo A*. A continuación, se explica en detalle cada método y atributo de esta clase.

### Atributos de la Clase

- **fila y col**: Representan la posición del nodo en la cuadrícula (fila y columna).
- **x y y**: Coordenadas x e y del nodo, calculadas multiplicando la fila y columna por el ancho del nodo.
- **color**: El color actual del nodo, utilizado para representar diferentes estados (por ejemplo, blanco para nodos no explorados, negro para paredes).
- **ancho**: El ancho del nodo en píxeles.
- **total_filas**: El número total de filas en la cuadrícula.
- **vecinos**: Una lista de nodos vecinos.

### Métodos de la Clase

- **__init__(self, fila, col, ancho, total_filas)**: Constructor de la clase que inicializa el nodo con su posición, tamaño y color.
- **get_pos(self)**: Devuelve la posición del nodo como una tupla `(fila, col)`.
- **es_pared(self)**: Verifica si el nodo es una pared (color negro).
- **es_inicio(self)**: Verifica si el nodo es el nodo de inicio (color naranja).
- **es_fin(self)**: Verifica si el nodo es el nodo final (color púrpura).
- **hacer_inicio(self)**: Establece el nodo como el nodo de inicio cambiando su color a naranja.
- **hacer_pared(self)**: Establece el nodo como una pared cambiando su color a negro.
- **hacer_fin(self)**: Establece el nodo como el nodo final cambiando su color a púrpura.
- **hacer_camino(self)**: Marca el nodo como parte del camino encontrado cambiando su color a púrpura.
- **hacer_visitado(self)**: Marca el nodo como visitado cambiando su color a rojo.
- **hacer_explorado(self)**: Marca el nodo como explorado cambiando su color a verde.
- **restablecer(self)**: Restablece el color del nodo a blanco, su estado inicial.
- **dibujar(self, ventana)**: Dibuja el nodo en la ventana de `pygame` con su color actual y su posición.
- **actualizar_vecinos(self, grid)**: Actualiza la lista de vecinos del nodo considerando movimientos cardinales (arriba, abajo, izquierda, derecha) y diagonales. Solo añade vecinos que no sean paredes.

## Funciones Adicionales
```python
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

```

### Heurística
- **heuristica(p1, p2)**: Esta función calcula la distancia Manhattan entre dos puntos `p1` y `p2`. La distancia Manhattan es la suma de las diferencias absolutas entre las coordenadas x e y de los puntos, es decir, la distancia a lo largo de los ejes de la cuadrícula. Esta distancia se utiliza en el algoritmo A* para estimar el costo de llegar del nodo actual al nodo final.

### Reconstrucción del Camino
- **reconstruir_camino(came_from, nodo_actual, dibujar)**: Esta función reconstruye el camino desde el nodo final al nodo inicial utilizando un diccionario `came_from` que contiene los nodos predecesores. Recorre el diccionario hacia atrás, marcando cada nodo en el camino con el color púrpura (indicando que es parte del camino) y redibujando la cuadrícula en cada paso.

### Algoritmo A*
- **algoritmo_a_star(dibujar, grid, inicio, fin)**: Esta función implementa el algoritmo A* para encontrar el camino más corto desde el nodo inicial al nodo final. Utiliza una cola de prioridad (`PriorityQueue`) para explorar los nodos basándose en su costo estimado total (`f_score`). La función realiza los siguientes pasos:
  1. Inicializa una cola de prioridad y añade el nodo de inicio.
  2. Define los diccionarios `g_score` y `f_score` para almacenar los costos g y f de cada nodo.
  3. Entra en un bucle que continúa hasta que la cola de prioridad esté vacía.
  4. Procesa eventos de `pygame` para permitir la interacción del usuario y la salida del programa.
  5. Extrae el nodo con el menor costo `f` de la cola de prioridad y lo remueve del conjunto de nodos abiertos.
  6. Si el nodo actual es el nodo final, reconstruye el camino y marca el nodo final.
  7. Para cada vecino del nodo actual, calcula el costo `g` temporal y, si es menor que el costo `g` actual del vecino, actualiza los costos `g` y `f` y añade el vecino a la cola de prioridad si no está ya presente.
  8. Marca el nodo actual como explorado y lo redibuja.
  9. Si el nodo actual no es el nodo de inicio, lo marca como visitado.
  10. Si no se encuentra un camino, la función devuelve `False`.

Estas funciones adicionales son esenciales para el funcionamiento del algoritmo A* y la visualización del proceso en la cuadrícula.


## Funciones para Crear y Dibujar la Cuadrícula
```python
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


```
### Crear la Cuadrícula

- **crear_grid(filas, ancho)**: Esta función crea una cuadrícula de nodos. Divide el ancho total de la ventana por el número de filas para determinar el ancho de cada nodo. Luego, crea una lista bidimensional de nodos, donde cada nodo es una instancia de la clase `Nodo`, con su posición específica en la cuadrícula.

### Dibujar la Cuadrícula

- **dibujar_grid(ventana, filas, ancho)**: Esta función dibuja las líneas de la cuadrícula en la ventana de `pygame`. Divide el ancho de la ventana por el número de filas para determinar el ancho de cada nodo y luego dibuja líneas horizontales y verticales en la cuadrícula para separar los nodos.

### Dibujar la Ventana

- **dibujar(ventana, grid, filas, ancho)**: Esta función dibuja la cuadrícula completa en la ventana de `pygame`. Primero llena la ventana con el color blanco. Luego, dibuja cada nodo de la cuadrícula llamando al método `dibujar` de la clase `Nodo`. Finalmente, dibuja las líneas de la cuadrícula y actualiza la pantalla.

### Obtener la Posición del Click

- **obtener_click_pos(pos, filas, ancho)**: Esta función traduce la posición del click del mouse en la ventana de `pygame` a una posición en la cuadrícula. Divide las coordenadas x e y del click por el ancho de cada nodo para determinar a qué fila y columna corresponde el click. Devuelve una tupla `(fila, columna)` que representa la posición en la cuadrícula.



## Función Principal
```python
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

```

### Función main

- **main(ventana, ancho)**: Esta es la función principal del programa que ejecuta el bucle principal de `pygame` y gestiona la interacción del usuario con la cuadrícula. A continuación, se explica en detalle cada parte de la función:

  1. **Inicialización**: 
     - Define el número de filas en la cuadrícula (`FILAS = 10`).
     - Crea la cuadrícula llamando a `crear_grid(filas, ancho)`.
     - Inicializa las variables `inicio` y `fin` como `None`, que serán usadas para almacenar los nodos de inicio y fin seleccionados por el usuario.

  2. **Bucle Principal**:
     - El bucle principal `while corriendo` se ejecuta continuamente hasta que el usuario cierre la ventana (`corriendo = False`).
     - Dentro del bucle, la función `dibujar` se llama para actualizar y mostrar la cuadrícula en la ventana.

  3. **Eventos de Usuario**:
     - El bucle `for event in pygame.event.get()` procesa los eventos generados por el usuario, como cerrar la ventana, hacer clic con el mouse o presionar una tecla.
     - **Cerrar la Ventana**: Si el evento es `pygame.QUIT`, se termina el bucle estableciendo `corriendo = False`.

  4. **Interacción con el Mouse**:
     - **Click Izquierdo**: Si el usuario hace clic izquierdo (`pygame.mouse.get_pressed()[0]`), se obtiene la posición del clic y se convierte en coordenadas de la cuadrícula usando `obtener_click_pos`. Dependiendo del estado actual, se pueden establecer los nodos de inicio y fin, o crear una pared en la posición seleccionada.
     - **Click Derecho**: Si el usuario hace clic derecho (`pygame.mouse.get_pressed()[2]`), se obtiene la posición del clic y se restablece el nodo en esa posición. Si el nodo restablecido era el nodo de inicio o fin, se restablecen las variables `inicio` o `fin` a `None`.

  5. **Interacción con el Teclado**:
     - Si el usuario presiona la barra espaciadora (`pygame.K_SPACE`) y tanto el nodo de inicio como el de fin están definidos, se actualizan los vecinos de cada nodo en la cuadrícula y se ejecuta el algoritmo A* llamando a `algoritmo_a_star`.

  6. **Salir del Programa**:
     - Después de salir del bucle principal, `pygame.quit()` se llama para cerrar la ventana y limpiar los recursos.

Esta función integra la creación de la cuadrícula, la visualización, y la interacción del usuario para permitir la ejecución y visualización del algoritmo A* en tiempo real.
