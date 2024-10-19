import requests
from bs4 import BeautifulSoup
import re
# URL de la página que deseas hacer scraping
url = 'https://www.sii.cl/ayudas/ayudas_por_servicios/1956-codigos-1959.html'

# Hacer una solicitud GET para obtener el contenido de la página
response = requests.get(url)

# Verificar que la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Crear una instancia de BeautifulSoup con el contenido de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    categorias = []
    for link in soup.find_all('font'):
        #Limpiar las palabras de simbolos extraños y espacios en blanco
        palabra = link.text.replace("\r\n","").replace("\xa0","")
        palabra = re.sub(r'\s{2,}', ' ', palabra)
        palabra = palabra.strip()
        categorias.append(palabra) # Se añade cada categoria al arreglo categorias

    print(f"Categorias: {categorias}")


else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")