import os
import shutil

def move_all_images_to_single_folder(input_folder, output_folder):
    """Mueve todas las imágenes de múltiples subcarpetas a una sola carpeta."""
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    counter = 0  # Contador para nombres únicos

    for root, _, files in os.walk(input_folder):
        for filename in files:
            # Generar un nuevo nombre para la imagen
            new_name = f"image_{counter:04d}{os.path.splitext(filename)[1]}"
            counter += 1

            # Ruta del archivo fuente y destino
            source_path = os.path.join(root, filename)
            destination_path = os.path.join(output_folder, new_name)

            # Mover la imagen
            shutil.move(source_path, destination_path)
            print(f"Movido: {source_path} -> {destination_path}")

# === MAIN ===
if __name__ == "__main__":
    INPUT_FOLDER = "predataset/chevrolet_el_camino"  # Carpeta raíz con subcarpetas de imágenes
    OUTPUT_FOLDER = "dataset/0"  # Carpeta donde se unificarán las imágenes
    
    move_all_images_to_single_folder(INPUT_FOLDER, OUTPUT_FOLDER)
    print("Movimiento de imágenes completo.")
