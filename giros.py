import requests
from bs4 import BeautifulSoup
import re

# URL de la página del SII de donde obtuve la información
url = 'https://www.sii.cl/ayudas/ayudas_por_servicios/1956-codigos-1959.html'

# Hacer una solicitud GET para obtener el contenido de la página
response = requests.get(url)

# Verificar que la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Crear una instancia de BeautifulSoup con el contenido de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Inicializar lista vacía para almacenar los datos en la estructura de diccionarios
    giros = []

    # Lista de categorías
    categorias = [
        'AGRICULTURA, GANADERÍA, SILVICULTURA Y PESCA',
        'EXPLOTACIÓN DE MINAS Y CANTERAS',
        'INDUSTRIA MANUFACTURERA',
        'SUMINISTRO DE ELECTRICIDAD, GAS, VAPOR Y AIRE ACONDICIONADO',
        'SUMINISTRO DE AGUA; EVACUACIÓN DE AGUAS RESIDUALES, GESTIÓN DE DESECHOS Y DESCONTAMINACIÓN',
        'CONSTRUCCIÓN',
        'COMERCIO AL POR MAYOR Y AL POR MENOR; REPARACIÓN DE VEHICULOS AUTOMOTORES Y MOTOCICLETAS',
        'TRANSPORTE Y ALMACENAMIENTO',
        'ACTIVIDADES DE ALOJAMIENTO Y DE SERVICIO DE COMIDAS',
        'INFORMACIÓN Y COMUNICACIONES',
        'ACTIVIDADES FINANCIERAS Y DE SEGUROS',
        'ACTIVIDADES INMOBILIARIAS',
        'ACTIVIDADES PROFESIONALES, CIENTIFICAS Y TÉCNICAS',
        'ACTIVIDADES DE SERVICIOS ADMINISTRATIVOS Y DE APOYO',
        'ADMINISTRACIÓN PÚBLICA Y DEFENSA; PLANES DE SEGURIDAD SOCIAL DE AFILIACIÓN OBLIGATORIA',
        'ENSEÑANZA',
        'ACTIVIDADES DE ATENCIÓN DE LA SALUD HUMANA Y DE ASISTENCIA SOCIAL',
        'ACTIVIDADES ARTÍSTICAS, DE ENTRETENIMIENTO Y RECREATIVAS',
        'OTRAS ACTIVIDADES DE SERVICIOS',
        'ACTIVIDADES DE LOS HOGARES COMO EMPLEADORES; ACTIVIDADES NO DIFERENCIADAS DE LOS HOGARES',
        'ACTIVIDADES DE ORGANIZACIONES Y ÓRGANOS EXTRATERRITORIALES'
    ]

    # Variable auxiliar para controlar la categoría actual, se asume la primera categoría inicialmente
    categoria_actual = categorias[0]  # Asumir la primera categoría del arreglo

    # Buscar las filas de la tabla (donde están los códigos y actividades)
    for link in soup.find_all('tr'):
        texto = link.text.strip().replace("\r\n", " ")
        texto = re.sub(r'\s{2,}', ' ', texto)  # Limpiar múltiples espacios

        # Buscar los códigos con formato numérico (ejemplo: 011101)
        match_codigo = re.match(r'\d{6}', texto)

        if match_codigo:  # Si encontramos un código (actividad real)
            # Dividir en código y el resto del texto
            partes = re.split(r'\s+', texto, maxsplit=2)

            if len(partes) >= 3:
                codigo = partes[0]  # El código es la primera parte
                nombre_actividad = partes[1] + " " + partes[2]  # El nombre es el resto

                # Limpiar el nombre para eliminar datos adicionales
                nombre_actividad = re.sub(r'(SI|NO|G)\s*\d\s*SI', '', nombre_actividad).strip()
                nombre_actividad = re.sub(r'(\n.*| G$)', '', nombre_actividad)

                # Extraer el primer "SI", "NO" o "G" que indica si está afecto a IVA
                match_iva = re.search(r'\b(SI|NO|G)\b', texto)
                iva_status = match_iva.group(0) if match_iva else "N/A"  # Valor por defecto en caso de no encontrar

                # Agregar los datos al arreglo de giros como diccionario
                giros.append({
                    "codigo": codigo,
                    "nombre": nombre_actividad,
                    "afecto_iva": iva_status,
                    "categoria": categoria_actual  # Asignar la categoría actual
                })
        else:

            for categoria in categorias:
                # Usar re.fullmatch para garantizar coincidencia exacta sin texto extra
                if re.fullmatch(re.escape(categoria), texto):
                    categoria_actual = categoria  # Actualizar la categoría
                    break

    # Mostrar los resultados
    print(giros)
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")