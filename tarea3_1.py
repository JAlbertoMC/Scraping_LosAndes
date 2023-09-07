import requests
from bs4 import BeautifulSoup
import csv
import codecs

url = 'https://www.losandes.com.pe'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todos los elementos con la clase "jeg_post_title" (títulos)
    titles = soup.find_all(class_='jeg_post_title')

    # Encuentra todos los elementos con la clase "jeg_meta_date" (fechas)
    dates = soup.find_all(class_='jeg_meta_date')

    # Verifica que haya títulos y fechas disponibles
    if titles and dates:
        # Abre un archivo CSV para escribir
        with open('losandes.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            archivo = csv.writer(csvfile)

            # Escribe el encabezado del CSV
            archivo.writerow(['TITULO', 'FECHA'])

            # Itera a través de los títulos y fechas y escribe en el CSV
            for title, date in zip(titles, dates):
                titulo_texto = title.get_text(strip=True)
                fecha_texto = date.get_text(strip=True)
                archivo.writerow([titulo_texto, fecha_texto])

        print("Archivo CSV creado correctamente.")
    else:
        print("No se encontraron títulos o fechas en la página.")
else:
    print("No se pudo acceder a la página:", response.status_code)
    print("No se pudo obtener el contenido de la página.")
