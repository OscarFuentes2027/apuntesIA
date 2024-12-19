from concurrent.futures import ThreadPoolExecutor
from bing_image_downloader import downloader
from serpapi import GoogleSearch

import requests
import os
from PIL import Image
import imagehash

# === CONFIGURACIÓN ===
SEARCH_QUERIES = [
    'Jeep Wrangler 2016 exterior',
    'Jeep Wrangler 2017 exterior',
    'Jeep Wrangler 2018 exterior',
    'Jeep Wrangler 2019 exterior',
    'Jeep Wrangler 2016-2019 modelo clásico',
    'Jeep Wrangler 2016 en exhibición de autos',
    'Jeep Wrangler 2017 off-road',
    'Jeep Wrangler 2018 en la calle',
    'Jeep Wrangler 2019 modificado',
    'Jeep Wrangler 2016-2019 vintage'
]

BING_LIMIT = 300  # Número de imágenes por búsqueda en Bing
GOOGLE_LIMIT = 300  # Número de imágenes por búsqueda en Google
OUTPUT_DIR = 'predataset/jeep_wrangler_2016_2019'  # Carpeta donde se guardarán las imágenes
GOOGLE_API_KEY = "f12216b5a994d905e6241ada742f9198b3917e056685a795222d0901a97fdfc6"

# === FUNCIONES ===
def download_images_from_bing(query):
    """Descarga imágenes desde Bing."""
    print(f"Descargando imágenes desde Bing para: {query}")
    downloader.download(query, limit=BING_LIMIT, output_dir=OUTPUT_DIR, adult_filter_off=True, force_replace=False, timeout=60, verbose=False)

def download_images_from_google(query):
    """Descarga imágenes desde Google usando SerpAPI."""
    print(f"Descargando imágenes desde Google para: {query}")
    search = GoogleSearch({
        "q": query,
        "tbm": "isch",
        "ijn": "0",
        "api_key": GOOGLE_API_KEY
    })
    results = search.get_dict()
    image_urls = [result['original'] for result in results.get('images_results', [])[:GOOGLE_LIMIT]]

    query_dir = os.path.join(OUTPUT_DIR, query.replace(' ', '_'))
    os.makedirs(query_dir, exist_ok=True)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(os.path.join(query_dir, f"google_{i}.jpg"), 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Error descargando {url}: {e}")


# === MAIN ===
if __name__ == "__main__":
    # Paralelizar descargas desde Bing y Google
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Bing descargas
        executor.map(download_images_from_bing, SEARCH_QUERIES)

        # Google descargas
        executor.map(download_images_from_google, SEARCH_QUERIES)


    print("Descarga completa y dataset limpio.")
