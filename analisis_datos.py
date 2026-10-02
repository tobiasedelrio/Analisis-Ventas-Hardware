import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Conectar a la base de datos que acabamos de crear
conn = sqlite3.connect('ecommerce.db')

# 2. Consultar la vista (View) usando una consulta SQL
# Aquí le pedimos a la base de datos que nos traiga el resumen ordenado de mayor a menor ingreso
query = "SELECT Categoria, Producto, Ingresos_Totales FROM vw_resumen_ventas ORDER BY Ingresos_Totales DESC;"
df_resultados = pd.read_sql_query(query, conn)

# 3. Mostrar los resultados en la terminal (como si fuera una tabla de Excel)
print("\n--- Resumen de Ingresos por Producto ---")
print(df_resultados)

# 4. Crear el gráfico de barras
plt.figure(figsize=(10, 6))
colores = ['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974']

# Le pasamos el eje X (Productos) y el eje Y (Ingresos Totales)
plt.bar(df_resultados['Producto'], df_resultados['Ingresos_Totales'], color=colores)

# Personalizar el gráfico para que se vea profesional
plt.title('Ingresos Totales por Producto', fontsize=14, fontweight='bold')
plt.xlabel('Productos', fontsize=12)
plt.ylabel('Ingresos Totales ($)', fontsize=12)
plt.xticks(rotation=15, ha='right') # Rotar los nombres para que se lean bien
plt.tight_layout()

# 5. Guardar el gráfico como imagen automáticamente (Ideal para el CV/GitHub)
plt.savefig('grafico_ventas.png')
print("\n¡Gráfico generado y guardado como 'grafico_ventas.png'!")

# 6. Mostrar el gráfico en una ventana y cerrar la conexión
plt.show()
conn.close()