import pygame
import random
import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from PIL import Image, ImageFilter, ImageEnhance
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow import keras
import pandas as pd
import os  # Para manejar operaciones del sistema de archivos


from sklearn.model_selection import train_test_split
import joblib  # Importar joblib para guardar y cargar modelos


# ------------------------ Inicialización de Pygame ------------------------


# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Define tu fuente 
fuente = pygame.font.Font(None, 36)

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# ------------------------ Carga de recursos ------------------------

# Cargar imágenes
jugador_frames = [
    pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\sprites\mono_frame_1.png'),
    pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\sprites\mono_frame_1.png')
]
bala_img = pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\sprites\purple_ball.png')
fondo_img = pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\game\fondo2.png')
nave_img = pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\game\ufo.png')
menu_img = pygame.image.load(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\game\menu.png')

# Escalar la imagen de fondo
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# ------------------------ Variables globales ------------------------




# Rectángulos iniciales
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Variables del jugador
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables de la bala
velocidad_bala = -10
bala_disparada = False

# Variables del fondo
fondo_x1 = 0
fondo_x2 = w

# Variables del menú y modos
pausa = False
menu_activo = True
modo_auto = False

datos_para_csv = [] 

# ------------------------ Definición de clases ------------------------

# Clase para manejar modelos
class ModelManager:
    def __init__(self):
        self.arbol = DecisionTreeClassifier()
        self.red_neuronal = None
        self.entrenado = False  # Inicializar como no entrenado

    def cargar_modelo_h5(self, filepath="modelo_red.h5"):
        try:
            self.red_neuronal = keras.models.load_model(filepath)
            self.red_neuronal.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self.entrenado = True
            print(f"Modelo de red neuronal cargado desde {filepath}.")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filepath}. Por favor, entrena y guarda un modelo primero.")
            self.entrenado = False

    def predecir_red(self, velocidad, distancia, umbral=0.5):
        print("Entrando a la función de predicción...")  # Confirmamos que entra aquí
        if not self.entrenado or self.red_neuronal is None:
            raise ValueError("El modelo de red neuronal no está entrenado.")
        
        # Convertimos la entrada a un array de NumPy
        entrada = np.array([[velocidad, distancia]])
        
        # Realizamos la predicción
        prediccion = self.red_neuronal.predict(entrada)[0][0]
        print(f"Predicción: {prediccion} (umbral: {umbral})")
        
        # Devolvemos el resultado según el umbral
        return 1 if prediccion >= umbral else 0




    def entrenar_arbol(self, datos):
        # Reiniciar el modelo de árbol existente
        self.arbol = DecisionTreeClassifier()
        self.entrenado = False  # Reiniciar estado de entrenamiento

        if len(datos) > 0:
            X, y = datos[:, :2], datos[:, 2]
            self.arbol.fit(X, y)
            self.entrenado = True
            print("Árbol entrenado correctamente.")
        else:
            print("No hay datos para entrenar.")

            
    def predecir_arbol(self, velocidad, distancia):
        if not self.entrenado:
            raise ValueError("El modelo no está entrenado.")
        return int(self.arbol.predict([[velocidad, distancia]])[0])
    
    def esta_entrenado(self):
        return self.entrenado
    
    
    
    def guardar_modelo(self, filepath="modelo_arbol.pkl"):
        if self.entrenado:
            joblib.dump(self.arbol, filepath)
            print(f"Modelo guardado en {filepath}.")
        else:
            print("El modelo no está entrenado, no se guardará.")

    def entrenar_arbol_desde_csv(self, filepath="dataset.csv"):
        try:
            # Reiniciar el modelo de árbol existente
            self.arbol = DecisionTreeClassifier()
            self.entrenado = False  # Reiniciar estado de entrenamiento

            # Leer el dataset desde el archivo CSV
            print(f"Intentando cargar el dataset desde: {filepath}")
            data = pd.read_csv(filepath)
            print(f"Dataset cargado desde {filepath}.")

            # Definir características (X) y etiquetas (y)
            X = data[["Velocidad", "Distancia"]].values
            y = data["Salto"].values

            # Dividir los datos en conjunto de entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Entrenar el árbol de decisiones
            self.arbol.fit(X_train, y_train)
            self.entrenado = True
            print("Árbol de decisiones entrenado correctamente.")

            # Guardar el modelo opcionalmente
            self.guardar_modelo("modelo_arbol.pkl")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filepath}. Asegúrate de generar y guardar un dataset primero.")
        except pd.errors.EmptyDataError:
            print(f"El archivo {filepath} está vacío o tiene un formato incorrecto.")
        except Exception as e:
            print(f"Ocurrió un error al entrenar el árbol de decisiones: {e}")



    def finalizar_juego_manual():
        global datos_para_csv
        if len(datos_para_csv) > 0:
            datos = np.array(datos_para_csv)
            print("Datos utilizados para entrenar:", datos)
            model_manager.entrenar_arbol(datos)
            guardar_arbol()
            print("Juego manual terminado. Modelo entrenado y guardado.")
        else:
            print("No hay datos suficientes para entrenar el modelo.")
        reiniciar_juego()
        
    def cargar_modelo(self, filepath="modelo_arbol.pkl"):
        try:
            self.arbol = joblib.load(filepath)
            self.entrenado = True
            print(f"Modelo cargado desde {filepath}.")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filepath}.")
    
    def entrenar_red_desde_csv(self, filepath="dataset.csv", modelo_guardado="modelo_red.h5"):
        try:
            # Leer el dataset desde el archivo CSV
            print(f"Intentando cargar el dataset desde: {filepath}")
            data = pd.read_csv(filepath)
            print(f"Dataset cargado desde {filepath}.")
            
            # Extraer las características y etiquetas
            X = data[["Velocidad", "Distancia"]].values
            y = data["Salto"].values
            
            # Dividir en conjuntos de entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Crear y entrenar el modelo de red neuronal
            self.red_neuronal = Sequential([
                Dense(16, input_dim=2, activation='relu'),
                Dense(8, activation='relu'),
                Dense(1, activation='sigmoid')
            ])
            self.red_neuronal.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self.red_neuronal.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)
            
            # Guardar el modelo entrenado
            self.red_neuronal.save(modelo_guardado)
            self.entrenado = True
            print(f"Modelo guardado en {modelo_guardado}.")
            
        except FileNotFoundError:
            print(f"No se encontró el archivo {filepath}. Asegúrate de generar y guardar un dataset primero.")
        except pd.errors.EmptyDataError:
            print(f"El archivo {filepath} está vacío o tiene un formato incorrecto.")
        except Exception as e:
            print(f"Ocurrió un error al entrenar el modelo: {e}")

    
    def entrenar_red(self, datos):
        if len(datos) > 0:
            X = datos[:, :2]
            y = datos[:, 2]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            self.red_neuronal = Sequential([
                Dense(16, input_dim=2, activation='relu'),
                Dense(8, activation='relu'),
                Dense(1, activation='sigmoid')
            ])
            self.red_neuronal.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self.red_neuronal.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)
            self.entrenado = True
        else:
            print("No hay datos para entrenar.")
        
model_manager = ModelManager()

# ------------------------ Definición de funciones ------------------------

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global modo_auto

    # Cargar la imagen de fondo y aplicarle desenfoque
    fondo_img = Image.open(r'C:\Users\Oscar Fuentes\Documents\proyectos\python\Actividad2\assets\game\fondo2.png')
    fondo_img = fondo_img.resize((w, h))  # Ajustar tamaño al de la ventana
    fondo_blur = fondo_img.filter(ImageFilter.GaussianBlur(10))  # Aplicar desenfoque

    # Oscurecer la imagen (reduce el brillo)
    enhancer = ImageEnhance.Brightness(fondo_blur)
    fondo_oscuro = enhancer.enhance(0.5)  # El valor 0.5 ajusta la oscuridad (0 = completamente negro, 1 = sin cambios)

    # Convertir la imagen procesada a Surface de Pygame
    fondo_oscuro_surface = pygame.image.fromstring(fondo_oscuro.tobytes(), fondo_oscuro.size, fondo_oscuro.mode)
    pantalla.blit(fondo_oscuro_surface, (0, 0))  # Dibujar la imagen desenfocada y oscurecida

    # Configurar fuentes
    fuente_titulo = pygame.font.Font(None, 48)
    fuente_opciones = pygame.font.Font(None, 36)

    # Dibujar título
    titulo = fuente_titulo.render("Menú Principal", True, BLANCO)
    pantalla.blit(titulo, (w // 2 - titulo.get_width() // 2, h // 2 - 140))

    # Opciones del menú
    lineas_texto = [
        "Presiona 'M': Modo Manual",
        "Presiona 'A': Modo Automático (Red Neuronal)",
        "Presiona 'W': Modo Automático (Árbol de Decisiones)",
        "Presiona 'R': Entrenar Árbol",
        "Presiona 'E': Entrenar Red Neuronal",
        "Presiona 'D': Guardar Dataset en CSV",
        "Presiona 'Q': Salir"
    ]

    # Renderizar opciones
    y = h // 2 - 100
    for linea in lineas_texto:
        texto = fuente_opciones.render(linea, True, BLANCO)
        pantalla.blit(texto, (w // 2 - texto.get_width() // 2, y))
        y += texto.get_height() + 10

    pygame.display.flip()

    # Lógica de eventos
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = "red"
                    model_manager.cargar_modelo_h5()
                    return
                if evento.key == pygame.K_w:
                    modo_auto = "arbol"
                    model_manager.cargar_modelo("modelo_arbol.pkl")
                    return
                if evento.key == pygame.K_m:
                    modo_auto = "manual"
                    return
                if evento.key == pygame.K_r:
                    model_manager.entrenar_arbol_desde_csv(filepath="dataset.csv")

                if evento.key == pygame.K_e:
                    model_manager.entrenar_red_desde_csv()
                if evento.key == pygame.K_d:
                    guardar_dataset()
                if evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

def entrenar_y_guardar_modelo(filepath="modelo_red.h5"):
    global datos_para_csv, model_manager

    if len(datos_para_csv) == 0:
        print("No hay datos suficientes para entrenar el modelo.")
        return

    # Convierte los datos recopilados a un array de NumPy
    datos = np.array(datos_para_csv)
    X, y = datos[:, :2], datos[:, 2]

    # Divide los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear y entrenar el modelo de red neuronal
    red_neuronal = Sequential([
        Dense(16, input_dim=2, activation='relu'),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    red_neuronal.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    red_neuronal.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)

    # Guarda el modelo entrenado en un archivo .h5
    red_neuronal.save(filepath)
    print(f"Modelo guardado en {filepath}.")



# Guardar el modelo del árbol en un archivo
def guardar_arbol(file_path="modelo_arbol.pkl"):
    global model_manager
    joblib.dump(model_manager.arbol, file_path)
    print(f"Modelo guardado en {file_path}.")

# Cargar el modelo del árbol desde un archivo
def cargar_arbol(file_path="modelo_arbol.pkl"):
    global model_manager
    try:
        model_manager.arbol = joblib.load(file_path)
        print(f"Modelo cargado desde {file_path}.")
    except FileNotFoundError:
        print(f"No se encontró el archivo {file_path}. Asegúrate de entrenar y guardar el modelo primero.")
        
# ------------------------ Funciones relacionadas con el juego ------------------------

import os  # Asegúrate de importar el módulo os

def guardar_dataset(filepath="dataset.csv"):
    global datos_para_csv
    if len(datos_para_csv) == 0:
        print("No hay datos para guardar.")
        return

    # Abrir el archivo en modo de escritura para sobrescribirlo
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(["Velocidad", "Distancia", "Salto"])
        # Escribir filas de datos
        writer.writerows(datos_para_csv)

    print(f"Dataset guardado en {filepath}.")

    # Limpiar datos después de guardarlos
    datos_para_csv = []
    print("Lista de datos para CSV limpiada.")



# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50
    bala_disparada = False

def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        if salto_altura > 0:
            # Ascendiendo  
            jugador.y -= salto_altura
            salto_altura -= gravedad
        else:
            # Descendiendo
            jugador.y += abs(salto_altura)
            salto_altura -= gravedad

        # Detectar aterrizaje
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            en_suelo = True
            salto_altura = 15  # Resetear altura de salto

    # Restringir la posición vertical del jugador
    if jugador.y < 0:
        print("Jugador alcanzó un límite superior, restringiendo.")
        jugador.y = 0






# Función para guardar datos del modelo
def guardar_datos():
    global jugador, bala, velocidad_bala, salto, datos_para_csv
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0

    # Imprimir los valores recopilados
    print(f"Guardando datos: Velocidad={velocidad_bala}, Distancia={distancia}, Salto={salto_hecho}")

    # Agregar los datos a la lista
    datos_para_csv.append((velocidad_bala, distancia, salto_hecho))



# Función para jugar automáticamente
def jugar_automatico():
    print("Modo automático activado")
    global salto, en_suelo, velocidad_bala, jugador, bala

    # Calcular las características actuales (velocidad y distancia)
    distancia = abs(jugador.x - bala.x)

    if modo_auto == "red":
        # Usar red neuronal
        if model_manager.entrenado and model_manager.red_neuronal:
            prediccion = model_manager.predecir_red(velocidad_bala, distancia)
            print(f"Predicción (Red Neuronal): {prediccion}")
        else:
            print("Red Neuronal no entrenada o no cargada.")
            return
    elif modo_auto == "arbol":
        # Usar árbol de decisiones
        if model_manager.entrenado:
            prediccion = model_manager.predecir_arbol(velocidad_bala, distancia)
            print(f"Predicción (Árbol de Decisiones): {prediccion}")
        else:
            print("Árbol de Decisiones no entrenado o no cargado.")
            return
    else:
        print("Modo automático desconocido.")
        return

    # Actuar según la predicción
    if prediccion == 1 and en_suelo:
        print("Saltando...")
        salto = True
        en_suelo = False

def perder_y_regresar_menu():
    global datos_para_csv, jugador, bala, nave, bala_disparada, salto, en_suelo

    # Puedes agregar una animación o mensaje de "Has perdido" aquí si deseas.
    print("Regresando al menú...")

    # Guardar datos antes de reiniciar el juego
    guardar_dataset()  # Guarda los datos en un archivo CSV

    # Reiniciar estado del juego sin borrar los datos recopilados
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True

    # Regresar al menú
    mostrar_menu()


    # Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    print("Datos recopilados para el modelo: ", datos_para_csv)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

# Función para actualizar el juego
def update():
    global fondo_x1, fondo_x2, bala, velocidad_bala

    # Mover los fondos para generar sensación de desplazamiento
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Dibujar y animar al jugador con su posición actual
    pantalla.blit(jugador_frames[0], (jugador.x, jugador.y))

    # Llama a disparar_bala() si la bala no ha sido disparada
    if not bala_disparada:
        disparar_bala()

    bala.x += velocidad_bala  # Mover la bala hacia la izquierda

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))  # Dibujar la bala

    # Detectar colisión entre el jugador y la bala
    if jugador.colliderect(bala):
        print("¡Colisión detectada!")
        reiniciar_juego()

    # Dibujar la nave (UFO)
    pantalla.blit(nave_img, (nave.x, nave.y))

def pausa_juego():
    global pausa
    pausa = not pausa  # Alterna el estado de pausa
    if pausa:
        print("Juego pausado.")
    else:
        print("Juego reanudado.")



# Función principal
def main():
    global salto, en_suelo, bala_disparada, modo_auto, datos_para_csv, pausa

    reloj = pygame.time.Clock()

    # Mostrar menú al inicio para seleccionar el modo
    mostrar_menu()

    correr = True
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Pausar o reanudar el juego
                    pausa_juego()
                if evento.key == pygame.K_o:  # Guardar el dataset en CSV
                    perder_y_regresar_menu()

        if not pausa:  # Solo ejecuta la lógica del juego si no está pausado
            if modo_auto == "red" or modo_auto == "arbol":
                jugar_automatico()
            elif modo_auto == "manual":
                guardar_datos()  # Guardar datos en modo manual
            manejar_salto()  # Manejar el salto
            update()  # Actualizar el estado del juego

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


# ------------------------ Ejecución principal ------------------------

if __name__ == "__main__":
  # Cargar el modelo si está disponible
    main()


