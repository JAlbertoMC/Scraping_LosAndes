import requests
from bs4 import BeautifulSoup
import csv
import codecs

url = 'https://www.losandes.com.pe'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titulos = soup.find_all(class_='jeg_post_title')
    fechas = soup.find_all(class_='jeg_meta_date')

    if titulos and fechas:
        # Abre un archivo CSV para escribir
        with open('Titular4.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            archivo = csv.writer(csvfile)

            # Escribe el encabezado del CSV
            archivo.writerow(['TITULAR DEL DIA', 'FECHA'])
            
            # Utiliza un conjunto para realizar un seguimiento de los datos ya agregados
            datos_agregados = set()

            # Itera a través de los títulos y fechas y escribe en el CSV
            for titulo, fecha in zip(titulos, fechas):
                titular_hoy = titulo.get_text(strip=True)
                fecha_titular = fecha.get_text(strip=True)
                
                # Verificar que en cada fila tenga TITULO Y FECHA 
                if titular_hoy and fecha_titular:
                    fila = (titular_hoy, fecha_titular)
                    if fila not in datos_agregados:
                        archivo.writerow([titular_hoy, fecha_titular])
                        datos_agregados.add(fila)
                    
        print("Archivo CSV creado correctamente.")
    else:
        print("No se encontraron títulos o fechas en la página.")
else:
    print("No se pudo acceder a la página:", response.status_code)
    print("No se pudo obtener el contenido de la página.")
