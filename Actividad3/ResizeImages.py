import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Ruta al modelo preentrenado
model_path = './ModelDensoFinal.keras'
model = load_model(model_path)

# Mapeo de clases
class_labels = {
    0: "chevrolet_el_camino",
    1: "chevrolet_express_cargo",
    2: "honda_acty",
    3: "jeep_wrangler_2016_2019",
    4: "Tesla Model 3"
}

def preprocess_image(image_path, target_size=(80, 80)):
    """
    Redimensiona y normaliza una imagen para que sea compatible con el modelo.
    """
    # Cargar la imagen
    image = cv2.imread(image_path)

    # Asegurarse de que la imagen sea RGB
    if image is None or len(image.shape) != 3:
        raise ValueError(f"La imagen no es válida o no es RGB: {image_path}")

    # Redimensionar la imagen
    resized_image = cv2.resize(image, target_size)

    # Normalizar los valores de los píxeles (0-1)
    normalized_image = resized_image / 255.0

    # Expandir dimensiones para el modelo
    image_batch = np.expand_dims(normalized_image, axis=0)

    return image_batch

def predict_image(input_path):
    """
    Procesa una imagen redimensionada y predice su clase usando el modelo.
    """
    # Preprocesar la imagen
    preprocessed_image = preprocess_image(input_path)

    # Realizar la predicción
    predictions = model.predict(preprocessed_image)

    # Obtener la clase y la confianza
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)

    # Etiqueta de clase
    class_label = class_labels.get(predicted_class, "Clase desconocida")

    return class_label, confidence

# Ejemplo de uso
#input_image_path = "C://Users//Oscar Fuentes//Desktop//pruebas//tesla//tesla1.jpg"  
input_image_path = "C://Users//Oscar Fuentes//Desktop//pruebas//Exxpress cargo/cargo3.jpg"  

try:
    predicted_label, confidence = predict_image(input_image_path)
    print(f"Predicción: {predicted_label} con una confianza de {confidence:.2f}")
except Exception as e:
    print(f"Error al procesar: {e}")
