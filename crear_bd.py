import sqlite3

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# 1. Diseño del Modelo Entidad-Relación
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Categorias (
        id_categoria INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        id_categoria INTEGER,
        FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
    );

    CREATE TABLE IF NOT EXISTS Ventas (
        id_venta INTEGER PRIMARY KEY,
        id_producto INTEGER,
        fecha_compra DATE NOT NULL,
        cantidad INTEGER NOT NULL,
        metodo_pago TEXT,
        FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
    );
''')

# 2. Limpiar datos anteriores (por si ejecutamos el script varias veces)
cursor.executescript('''
    DELETE FROM Ventas;
    DELETE FROM Productos;
    DELETE FROM Categorias;
''')

# 3. Insertar el nuevo catálogo de Hardware
cursor.executescript('''
    INSERT INTO Categorias (id_categoria, nombre) VALUES 
    (1, 'Componentes de PC'), (2, 'Periféricos y Monitores');

    INSERT INTO Productos (id_producto, nombre, precio, id_categoria) VALUES 
    (1, 'Tarjetas Gráficas', 450.00, 1),
    (2, 'Monitores Gamer', 180.00, 2),
    (3, 'Teclados Mecánicos', 50.00, 2),
    (4, 'Auriculares Inalámbricos', 40.00, 2),
    (5, 'Gabinetes', 80.00, 1);

    -- Simulamos algunas ventas recientes
    INSERT INTO Ventas (id_venta, id_producto, fecha_compra, cantidad, metodo_pago) VALUES 
    (1, 1, '2026-10-01', 2, 'Transferencia'),
    (2, 2, '2026-10-01', 4, 'QR'),
    (3, 3, '2026-10-02', 5, 'QR'),
    (4, 4, '2026-10-02', 3, 'Tarjeta de Crédito'),
    (5, 5, '2026-10-03', 2, 'Transferencia'),
    (6, 2, '2026-10-04', 2, 'QR'),
    (7, 1, '2026-10-05', 1, 'Tarjeta de Crédito');
''')

# 4. Crear o actualizar la vista
cursor.executescript('''
    DROP VIEW IF EXISTS vw_resumen_ventas;
    CREATE VIEW vw_resumen_ventas AS
    SELECT 
        c.nombre AS Categoria,
        p.nombre AS Producto,
        SUM(v.cantidad) AS Total_Vendidos,
        SUM(v.cantidad * p.precio) AS Ingresos_Totales
    FROM Ventas v
    JOIN Productos p ON v.id_producto = p.id_producto
    JOIN Categorias c ON p.id_categoria = c.id_categoria
    GROUP BY c.nombre, p.nombre;
''')

conn.commit()
conn.close()

print("¡Éxito! La base de datos fue actualizada con el nuevo catálogo de Hardware.")