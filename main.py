from mcp.server.fastmcp import FastMCP
import csv
import os
from planilla import agregar_gasto, obtener_gastos, eliminar_gasto, generar_csv

print("Starting MCP server...")

# Create an MCP server
mcp = FastMCP("hackathon-demo")

@mcp.tool()
def agregar_gasto_tool(articulo: str, cantidad: int, precio: int, categoria: str, fecha: str)-> str:
    """
    Agrega un gasto a la hoja de cálculo.
    
    Argumentos:
    articulo: Nombre del artículo preferentemente, en caso de no aparecer, nombre de la tienda. En caso de hacer referencia a un ingreso, se debe especificar el nombre del ingreso.
    cantidad: Cantidad del artículo.
    precio: Precio del artículo.
    categoria: Categoría del gasto perteneciente a alguna de las siguientes clases segun lo que mejor se ajuste: salud, entretenimiento, alimentos, regalos, educacion, personales, vivienda, ingresos y otros. En caso de corresponder a un articulo que hace referencia a un ingreso, se debe adjudicar a la categoría de ingresos o consultar al usuario antes de agregar.
    fecha: Es importante formatear la fecha que ingresa el usuario para que se cumpla el formato 'DD-MM-YYYY' a la hora de insertar a la planilla.

    Devuelve:
    Un mensaje de confirmación con el número de celdas actualizadas.
    """
    result = agregar_gasto(articulo, cantidad, precio, categoria, fecha)
    return f"Gasto agregado: {result.get('updates').get('updatedCells')} celdas actualizadas."

@mcp.tool()
def obtener_gastos_tool() -> str:
    """
    Obtiene TODOS los gastos de la hoja de cálculo.
    
    Devuelve:
    Lista de todos los gastos.
    """
    return obtener_gastos()

@mcp.tool()
def eliminar_gasto_tool(articulo: str, fecha: str) -> str:
    """
    Elimina un gasto específico de la hoja de cálculo a partir del nombre y de la fecha. 
    Importante confirmar con el usuario que desea eliminar el gasto antes de invocar la funcion. 
    Es necesario invocar la funcion obtener_gastos_tool() con el objetivo de interpretar el nombre del gasto a eliminar ya que el usuario puede ser inpreciso con el nombre.
    
    Argumentos:
    articulo: Nombre del artículo a eliminar, llamar a obtener_gastos_tool() para verificar que gasto corresponde con el nombre exacto.
    fecha: Fecha del gasto a eliminar en formato 'DD-MM-YYYY'.

    Devuelve:
    Mensaje de confirmación o error.
    """
    result = eliminar_gasto(articulo, fecha)
    return result

@mcp.tool()
def descargar_plantilla_tool() -> str:
    """
    Descarga la plantilla de gastos en formato CSV en la carpeta Descargas del usuario.
    """
    values = generar_csv()
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads", "plantilla_gastos.csv")

    with open(downloads_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in values:
            writer.writerow(row)
    
    return f"Plantilla descargada en {downloads_path}"