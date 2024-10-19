import csv

# Define el nombre del archivo CSV
nombre_archivo = 'giros.csv'

# Abre el archivo en modo de escritura
with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
    # Crea un objeto writer
    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=giros[0].keys())

    # Escribe la cabecera (nombres de las columnas)
    escritor_csv.writeheader()

    # Escribe las filas
    escritor_csv.writerows(giros)

print(f'Datos exportados a {nombre_archivo} con éxito.')