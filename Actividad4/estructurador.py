import os
import json

# Ruta a la carpeta con los archivos .txt
txt_folder = "./limpios"

# Crear una lista para almacenar los datos procesados
dataset = []

# Verificar que la carpeta exista
if not os.path.exists(txt_folder):
    raise FileNotFoundError(f"La carpeta {txt_folder} no existe.")

# Leer todos los archivos .txt
for filename in os.listdir(txt_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(txt_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            dataset.append({"prompt": f"Contenido de {filename}", "response": content})

# Guardar como JSONL
output_file = "./dataset.jsonl"  # Cambié el nombre de salida
with open(output_file, "w", encoding="utf-8") as f:
    for entry in dataset:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"Dataset guardado en {output_file}")
