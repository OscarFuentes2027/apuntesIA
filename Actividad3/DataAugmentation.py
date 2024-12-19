import os
import tensorflow as tf
import numpy as np

# Directorios de entrada y salida
input_dir = './dataset/4'
output_dir = './DataAug/4'

# Crear carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Listar todas las imágenes en el directorio de entrada
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

def rotate_image(image, angle_degrees):
    """
    Rota una imagen en el ángulo dado en grados.
    """
    # Convertir el ángulo de grados a radianes
    angle_radians = angle_degrees * np.pi / 180.0

    # Obtener las dimensiones de la imagen
    image_shape = tf.shape(image)
    height, width = tf.cast(image_shape[0], tf.float32), tf.cast(image_shape[1], tf.float32)

    # Calcular el centro de la imagen
    center_x, center_y = width / 2.0, height / 2.0

    # Crear la matriz de transformación para la rotación
    cos_val = tf.cos(angle_radians)
    sin_val = tf.sin(angle_radians)

    # Definir la transformación en el formato requerido [a, b, c, d, e, f, g, h]
    transform = [
        cos_val, -sin_val, (1 - cos_val) * center_x + sin_val * center_y,
        sin_val,  cos_val, (1 - cos_val) * center_y - sin_val * center_x,
        0, 0
    ]

    # Aplicar la transformación usando ImageProjectiveTransformV2
    transform = tf.convert_to_tensor([transform], dtype=tf.float32)  # Forma (1, 8)
    image = tf.raw_ops.ImageProjectiveTransformV2(
        images=tf.expand_dims(image, 0),
        transforms=transform,
        output_shape=image_shape[:2],
        interpolation="BILINEAR"
    )
    return tf.squeeze(image, 0)  # Quitar la dimensión batch

def flip_image(image):
    """
    Aplica un reflejo horizontal a la imagen.
    """
    return tf.image.flip_left_right(image)

def save_image(image, path, ext):
    """
    Guarda una imagen en el formato adecuado según su extensión.
    """
    if ext.lower() == '.png':
        tf.io.write_file(path, tf.io.encode_png(image))
    else:
        tf.io.write_file(path, tf.io.encode_jpeg(image))

for img_name in image_files:
    input_path = os.path.join(input_dir, img_name)

    try:
        # Leer la imagen
        image_raw = tf.io.read_file(input_path)
        image = tf.io.decode_image(image_raw, channels=3, dtype=tf.uint8)

        # Guardar la imagen original
        base_name, ext = os.path.splitext(img_name)
        original_output_path = os.path.join(output_dir, f"original_{base_name}{ext}")
        save_image(image, original_output_path, ext)

        # Guardar la imagen original reflejada
        flipped_original = flip_image(image)
        flipped_original_output_path = os.path.join(output_dir, f"original_flipped_{base_name}{ext}")
        save_image(flipped_original, flipped_original_output_path, ext)

        # Generar 10 imágenes rotadas y sus versiones reflejadas
        for i in range(5):
            angle_degrees = i * 15  # Incremento de 15 grados
            rotated_image = rotate_image(image, angle_degrees)

            # Guardar la imagen rotada
            rotated_output_path = os.path.join(output_dir, f"rot_{base_name}_{i}{ext}")
            save_image(rotated_image, rotated_output_path, ext)

            # Crear y guardar la versión reflejada de la imagen rotada
            flipped_rotated_image = flip_image(rotated_image)
            flipped_rotated_output_path = os.path.join(output_dir, f"rot_flipped_{base_name}_{i}{ext}")
            save_image(flipped_rotated_image, flipped_rotated_output_path, ext)

    except tf.errors.InvalidArgumentError as e:
        print(f"Error al procesar el archivo {input_path}: {e}")

print("Rotaciones, reflejos y copias de originales completadas. Imágenes guardadas en:", output_dir)