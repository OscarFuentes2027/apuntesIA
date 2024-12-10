<h1 style="text-align: center;"> Fundamentación sobre la Reforma al Poder Judicial y Organismos Autónomos</h1>
<hr>
<h2 style="text-align: center;">Actividad 4</h2>
<p style="text-align: center;">Proyecto realizado por: Oscar Fuentes</p>


## Índice

1. [Introducción](#introducción)
2. [Herramientas empleadas](#herramientas-empleadas)
3. [Algoritmos implementados](#algoritmos-implementados)
    -  [Algoritmo de limpieza de texto](#algoritmo-de-limpieza-de-texto)
      - [Explicación del limpiador](#explicación-del-limpiador)
      - [Código del limpiador](#código-del-limpiador)
4. [Generador de JSONL](#generador-de-jsonl)
   - [Explicación del estructurador](#explicación-del-estructurador)
   - [Código del generador de JSONL](#código-del-generador-de-jsonl)
5. [Conversión a CSV para LLaMA 3.2](#conversión-a-csv-para-llama-32)
   - [Explicación del script](#explicación-del-script)
   - [Código para la conversión](#código-para-la-conversión)
6. [Uso de Ollama para análisis avanzado](#uso-de-ollama-para-análisis-avanzado)
   - [Instalación de Ollama](#instalación-de-ollama)
   - [GUI con AnythingLLM](#gui-con-anythingllm)
7. [Conclusión](#conclusión)



## Introducción

Para esta práctica, tuve que investigar de maneras inusuales y, en ciertos casos, poco convencionales. Esto implicó emplear diversos algoritmos para profundizar en el tema. Como primer paso, decidí recopilar una amplia cantidad de investigaciones sobre el tema en cuestión: en total, descargué 16 documentos. Estos textos presentaban un sesgo político mayormente neutral, aunque algunos mostraban posturas a favor y otros en contra. Esta selección equilibrada tenía como propósito garantizar que la información fuera lo más objetiva posible, permitiéndome formar mi propio criterio.

Además, consulté fuentes reconocidas y confiables, basándome en su contenido para enriquecer mi análisis. Para ello, utilicé técnicas de scraping en dichas páginas web y procesé la información obtenida con el modelo **LLaMA 3.2**, asegurando que la interpretación de los datos fuera precisa. Más adelante, abordaré en detalle el uso de esta herramienta.

## Herramientas empleadas

Para llevar a cabo el análisis, utilicé varias herramientas específicas:

1. **BeautifulSoup**: para realizar scraping en las páginas web.
2. **pdfplumber**: para extraer información de documentos PDF.
3. **Ollama**: específicamente con **LLaMA 3.2**, para analizar y profundizar en el contenido recopilado.

## Algoritmos implementados

Entre los algoritmos desarrollados, destaco uno diseñado para limpiar caracteres extraños presentes en los datos extraídos mediante web scraping y en los documentos procesados desde los PDFs. Este algoritmo tuvo un papel crucial en la normalización de la información para su análisis posterior. A continuación, presento el código utilizado: 

```python
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
```

## Algoritmo de limpieza de texto

El siguiente código implementa un limpiador de texto que elimina elementos no deseados como saltos de línea múltiples, encabezados repetitivos y espacios en blanco innecesarios. Esto se hace para normalizar el texto antes de procesarlo.

### Explicación del limpiador

1. **Eliminar saltos de línea múltiples**: 
   Se utiliza la función `re.sub(r'\n+', '\n', text)` para reemplazar múltiples saltos de línea consecutivos por un único salto.
   
2. **Eliminar encabezados o pies de página repetitivos**: 
   Con `re.sub(r'(Página\s\d+)', '', text)` se eliminan patrones como "Página 1" o "Página 2", que podrían estar presentes en documentos generados automáticamente.

3. **Eliminar espacios en blanco adicionales**: 
   Se aplica `re.sub(r'\s+', ' ', text)` para reemplazar múltiples espacios consecutivos por un solo espacio.

4. **Guardar los textos limpios**: 
   Cada archivo procesado se guarda en una carpeta separada (`./limpios`) para facilitar el acceso en etapas posteriores.

### Código del limpiador

```python
import os
import re

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
```

Todos los textos limpiados fueron guardados en una carpeta llamada `limpios`. Esto permite usarlos posteriormente en el creador de JSON, que estructura cada archivo limpio en un único archivo `JSONL`, listo para ser usado como dataset.

---

## Generador de JSONL

El siguiente código toma los textos limpios y los organiza en un formato JSONL. Cada archivo `.txt` se convierte en un objeto JSON con un campo `prompt` que indica el origen del texto y un campo `response` que contiene el contenido del archivo.

### Explicación del estructurador

1. **Leer los archivos limpios**:
   El programa recorre todos los archivos en la carpeta `./limpios` y los abre para extraer su contenido.

2. **Crear entradas JSON**:
   Cada archivo se convierte en una entrada con dos campos:
   - `prompt`: Describe la fuente del contenido.
   - `response`: Contiene el texto del archivo.

3. **Guardar en formato JSONL**:
   Cada entrada se escribe en un archivo `dataset.jsonl`. Este formato es ideal para datasets grandes, ya que cada línea del archivo representa un objeto JSON independiente.

### Código del generador de JSONL

```python
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
output_file = "./dataset.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for entry in dataset:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(f"Dataset guardado en {output_file}")
```

El archivo resultante, `dataset.jsonl`, contiene un dataset consolidado con los textos procesados, listo para ser utilizado en modelos de análisis o entrenamiento de inteligencia artificial.


## Conversión a CSV para LLaMA 3.2

Para integrar el dataset procesado con el modelo **LLaMA 3.2**, convertí el archivo JSON en un archivo CSV utilizando el siguiente script:

### Explicación del script

1. **Cargar datos desde JSON**: 
   Se usa la biblioteca `pandas` para cargar el archivo `textos_procesados.json` y manejarlo como un DataFrame.

2. **Guardar en formato CSV**: 
   Con `data.to_csv()`, el contenido del JSON se convierte y guarda en un archivo CSV, asegurando que sea compatible con herramientas adicionales.

3. **Configuración de rutas**: 
   El script permite definir tanto rutas relativas como absolutas para mayor flexibilidad.

### Código para la conversión

```python
import pandas as pd

# Ruta al archivo JSON
json_file = "textos_procesados.json"  # Ruta relativa o absoluta del archivo JSON

# Cargar datos del JSON
data = pd.read_json(json_file)

# Ruta para guardar el archivo CSV
csv_file = "textos_procesados.csv"  # Guarda en el directorio actual

# Convertir a CSV
data.to_csv(csv_file, index=False, encoding='utf-8')

print(f"Archivo convertido y guardado en: {csv_file}")
```

Con este código, el dataset quedó listo para ser utilizado con herramientas avanzadas, como **Ollama**.

---

## Uso de Ollama para análisis avanzado

**Ollama** fue la herramienta clave para analizar el tema a profundidad. Con el CSV generado, pude integrar toda la información en **LLaMA 3.2** para obtener respuestas confiables y detalladas. 

### Instalación de Ollama

Para instalar **Ollama**, simplemente accedí a su [página oficial](https://ollama.ai/) y descargué la herramienta. Después, en la sección de *Models*, descargué el modelo **LLaMA 3.2**.

### GUI con AnythingLLM

Dado que Ollama funciona principalmente desde la consola, instalé **AnythingLLM**, una interfaz gráfica que facilita el uso de modelos como LLaMA. 

1. **Subida del CSV**: 
   En **AnythingLLM**, cargué el archivo CSV generado. Este paso permitió que la herramienta procesara el dataset y generara embeddings.

2. **Generación de respuestas**: 
   Con los embeddings creados, **Ollama** pudo responder preguntas basadas en el dataset, ayudándome a analizar la información de manera eficiente y precisa.

---

## Respuestas a las preguntas



Primero, consulté a **Ollama** para obtener una perspectiva inicial. A continuación, se muestra la respuesta generada (puedes insertar la imagen aquí):  
![Respuesta inicial de Ollama](/Actividad4/images/image.png)  

Como podemos observar, las respuestas son concisas y directas. Sin embargo, para profundizar en el tema, solicité que elaborara más sobre cada aspecto. Mi análisis es el siguiente:

### 1. ¿El diagnóstico de la ley al poder judicial es conocido y qué estudios expertos se tuvieron en cuenta?

**Respuesta: NO**  
A pesar de utilizar un total de 22 documentos en el dataset, parece que no se dispone de información suficiente sobre los estudios utilizados para fundamentar el diagnóstico. Esto indica que el diagnóstico específico podría no ser ampliamente conocido o discutido. No obstante, el tema general del poder judicial sí es objeto de debate en diversas fuentes. Por ejemplo, documentos como *"Reforma integral al sistema de justicia en México: desafíos y propuestas"* subrayan la importancia de mejorar la eficiencia del sistema judicial, mientras que *"Desafíos y propuestas para la reforma del Poder Judicial"* destaca la necesidad de mayor transparencia en la selección de jueces y magistrados.

### 2. ¿Por qué la reforma no incluyó a las fiscalías y a la defensoría, limitándose solo al poder judicial?

**Respuesta: Porque muy posiblemente haya una expansión en la reforma o haya específicas para ellas**
Existe una alta probabilidad de que se esté considerando realizar una reforma específica para las fiscalías y la defensoría en el futuro, o incluso una reforma mucho más amplia que abarque todos los actores del sistema de justicia. Esto se deduce de documentos como *“Comisiones: el Senado aprobó hoy las tres iniciativas para reglamentar la reforma al Poder Judicial”*, donde se plantean diversos factores en juego.

Asimismo, el documento *“Reforma integral al sistema de justicia en México: desafíos y propuestas”* resalta la importancia de mejorar la coordinación entre todos los actores del sistema, incluyendo fiscalías y defensoría. Aunque su rol puede percibirse como más técnico y de apoyo, en contraste con la función jurisdiccional del poder judicial, es indiscutible que desempeñan un papel clave en la aplicación de la ley y la protección de los derechos humanos. Esta aparente contradicción sugiere que su inclusión en futuras reformas es esencial.

### 3. ¿Qué medidas concretas se implementarán para evitar la captación del crimen organizado y la violencia en el contexto electoral?

Las medidas planteadas para abordar este problema incluyen:

1. **Aumento de la seguridad durante campañas electorales**:  
   - Implementación de mecanismos adicionales de protección, como la presencia de guardias de seguridad y la monitorización activa de redes sociales.

2. **Colaboración interinstitucional**:  
   - Coordinación entre las autoridades electorales y las fuerzas del orden para prevenir actos de intimidación dirigidos hacia candidatos y votantes.

3. **Fortalecimiento en la recopilación de pruebas**:  
   - Desarrollo de estrategias para documentar y presentar evidencias sobre la participación del crimen organizado en actividades ilegales durante los procesos electorales.

4. **Actualización de leyes y regulaciones**:  
   - Creación e implementación de marcos legales que garanticen la protección de candidatos y votantes contra intimidaciones y manipulaciones.



---
## Conclusión

La combinación de herramientas como **BeautifulSoup**, **pdfplumber**, **pandas**, y **Ollama** con el modelo **LLaMA 3.2** permitió procesar, estructurar y analizar una gran cantidad de información de forma organizada y efectiva. Esto no solo simplificó el análisis, sino que también garantizó que las respuestas fueran confiables y basadas en datos previamente curados.
```