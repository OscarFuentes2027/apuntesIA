import pdfplumber
import os

# Ruta del directorio donde están los PDFs
pdf_dir = "./general_organismos_autonomos"
output_dir = "./general_or_text"
os.makedirs(output_dir, exist_ok=True)

# Iterar sobre todos los archivos PDF
for pdf_file in os.listdir(pdf_dir):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        output_path = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.txt")
        
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        # Guardar texto en un archivo .txt
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Texto extraído y guardado en: {output_path}")
