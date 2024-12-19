import requests
from bs4 import BeautifulSoup

# URL del sitio web
url = "https://www.msn.com/es-mx/noticias/mexico/comisiones-del-senado-aprueban-tres-nuevas-leyes-de-la-reforma-al-poder-judicial/ar-AA1vhnNP"

# Realizar la solicitud HTTP sin verificar el certificado
response = requests.get(url, verify=False)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extraer texto de los párrafos
    paragraphs = soup.find_all('p')
    
    # Abrir un archivo de texto para escribir los párrafos
    with open("texto_extraido7.txt", "w", encoding="utf-8") as file:
        for p in paragraphs:
            file.write(p.get_text(strip=True) + "\n")
    print("Texto guardado en 'texto_extraido7.txt'")
else:
    print(f"No se pudo acceder al sitio: {url}")
