from google.oauth2 import service_account
from googleapiclient.discovery import build

#Configuracion de hoja
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1nKHpZmHxqSv3ZggKS4t3bck3yvtbiRAU_psI3hEIKhc'
RANGE = 'Hoja 1!A:E'

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        'credenciales.json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    # Esto nos va a devolver el servicio con los metodos que necesitamos para el programita
    return service.spreadsheets().values()

def agregar_gasto(articulo : str, cantidad : int, precio : float, categoria : str, fecha : str):
    service = get_service()
    values = [[articulo, cantidad, precio, categoria, fecha]]
    body = {'values': values}
    result = service.append(spreadsheetId=SPREADSHEET_ID, range=RANGE, body=body, valueInputOption='USER_ENTERED').execute()
    return result

def eliminar_gasto(articulo: str, fecha: str) -> str:
    service = get_service()
    result = service.get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()

    values = result.get("values", [])
    if not values or len(values) <= 1:
        return "La hoja está vacía."

    headers = values[0]
    datos = values[1:]

    # Buscar índice de la fila a eliminar
    for i, fila in enumerate(datos, start=2):  # start=2 porque A1 es encabezado
        fila_dict = dict(zip(headers, fila))
        if (
            fila_dict.get("Articulo", "").lower() == articulo.lower()
            and fila_dict.get("Fecha", "") == fecha
        ):
            service.clear(spreadsheetId=SPREADSHEET_ID, range=f"Hoja 1!A{i}:E{i}").execute()
            return f"Gasto eliminado: Articulo '{articulo}', Fecha '{fecha}' (fila {i})"

    return f"No se encontró ningún gasto con artículo '{articulo}' y fecha '{fecha}'."

def obtener_gastos():
    service = get_service()
    result = service.get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    values = result.get('values', [])
    if not values:
        return "No hay gastos registrados."

    titulos = values[0]
    gastos = values[1:]

    datos_formateados = []

    for gasto in gastos:
        fila = []
        for titulo, valor in zip(titulos, gasto):
            fila.append(f"{titulo}: {valor}")
        texto = ", ".join(fila)
        datos_formateados.append(texto)
    
    return "\n".join(datos_formateados)

def generar_csv():
    service = get_service()
    result = service.get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    return result.get("values", [])