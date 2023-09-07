import requests
from bs4 import BeautifulSoup
import csv
import codecs

url = 'https://www.losandes.com.pe'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # BUSCA ELEMENTOS CON CLASE "jeg_post_titulo" para titulos
    titulos = soup.find_all(class_='jeg_post_title')

    # BUSCA ELEMENTOS CON CLASE "jeg_meta_fecha" para fechas
    fechas = soup.find_all(class_='jeg_meta_date')

    # Verifica que haya títulos y fechas disponibles
    if titulos and fechas:
        # Abre un archivo CSV para escribir
        with open('Titulares_LosAndes.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            archivo = csv.writer(csvfile)

            # Escribe el encabezado del CSV
            archivo.writerow(['TITULAR DEL DIA', 'FECHA'])

            # Itera a través de los títulos y fechas y escribe en el CSV
            for titulo, fecha in zip(titulos, fechas):
                titular_hoy = titulo.get_text(strip=True)
                fecha_titular = fecha.get_text(strip=True)
                archivo.writerow([titular_hoy, fecha_titular])

        print("Archivo CSV creado correctamente.")
    else:
        print("No se encontraron títulos o fechas en la página.")
else:
    print("No se pudo acceder a la página:", response.status_code)
    print("No se pudo obtener el contenido de la página.")
