import re
import pdfplumber
import os

# Función para limpiar texto
def clean_text(text):
    # Eliminar saltos de línea múltiples
    text = re.sub(r'\n+', '\n', text)
    # Quitar encabezados o pie de página (si tienen un patrón)
    text = re.sub(r'(Página\s\d+)', '', text)
    # Eliminar espacios en blanco extra
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Limpiar todos los textos
text_dir = "./web"
clean_dir = "./limpios"
os.makedirs(clean_dir, exist_ok=True)

for text_file in os.listdir(text_dir):
    if text_file.endswith(".txt"):
        text_path = os.path.join(text_dir, text_file)
        with open(text_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        cleaned_text = clean_text(raw_text)
        
        # Guardar texto limpio
        output_path = os.path.join(clean_dir, text_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
        print(f"Texto limpio guardado en: {output_path}")
