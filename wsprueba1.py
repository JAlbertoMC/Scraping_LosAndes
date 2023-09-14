import requests
from bs4 import BeautifulSoup
from collections import deque
import mysql.connector

# En esta lista crearemos un registro de los enlaces para evitar duplicidad
enlaces_explorados = set()

# Conéctate a la base de datos
def conectar_base_de_datos():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            # Crear base de datos en PHPMyAdmin
            database='midba'
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

# Inserta un resultado en la base de datos
def insertar_resultado(palabra_clave, links, detalles, fecha, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabla_de_resultados (palabra_clave, links, detalles, fecha) VALUES (%s, %s, %s, %s)",
                       (palabra_clave, links, detalles, fecha))
        conn.commit()
        cursor.close()
    except Exception as e:
        print("Error al insertar datos en el DB:", e)

def buscar_palabra_clave(palabra_clave, links, conn):
    response = requests.get(links)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #Buscar en divs con clase content-inner
        div_contenido = soup.find('div', class_='content-inner')

        if div_contenido:
            detalles = '\n'.join(p.text for p in div_contenido.find_all('p'))
        else:
            detalles = ""

        entry_header = soup.find('div', class_='entry-header')
        if entry_header:
            fecha = entry_header.find('div', class_='jeg_meta_date').text.strip()
        else:
            fecha = ""

        if palabra_clave in detalles:
            print(palabra_clave, "URL encontrado:", links)
            insertar_resultado(palabra_clave, links, detalles, fecha, conn)
        else:
            print("palabra no encontrada en la URL:", links)

    else:
        print("Error al acceder a la URL", links)

def explorar_enlaces(links_inicial, nivel_maximo, conn):
    cola = deque([(links_inicial, 0)])

    while cola:
        links_actual, nivel_actual = cola.popleft()
        enlaces_explorados.add(links_actual)

        if nivel_actual <= nivel_maximo:
            response = requests.get(links_actual)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                enlaces = soup.find_all('a', href=True)

                for cada_enlace in enlaces:
                    enlace_links = cada_enlace['href']

                    if enlace_links.startswith('http') and enlace_links not in enlaces_explorados:
                        cola.append((enlace_links, nivel_actual + 1))
                        enlaces_explorados.add(enlace_links)
                        buscar_palabra_clave("JULIACA", enlace_links, conn)

# Cambia los valores con tu configuración
conn = conectar_base_de_datos()
if conn is not None:
    explorar_enlaces("https://www.losandes.com.pe", 10, conn)
    conn.close()
else:
    print("No se pudo conectar a la base de datos.")
