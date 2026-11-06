import csv
import os
import time

from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_separate_chaining as mp
from DataStructures.Tree import red_black_tree as rbt

# Evita problemas de buffer al leer el CSV (recomendado en el enunciado)
csv.field_size_limit(2147483647)

# Carpeta de datos: <proyecto>/Data/Data (el repo trae los CSV dentro de Data/Data).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIRS = (os.path.join(BASE_DIR, "..", "Data", "Data"), os.path.join(BASE_DIR, "..", "Data"))

COLUMNAS_REQUERIDAS = ("order_id", "order_date", "brand", "model_name", "category", "gender",
                       "size", "color", "base_price_usd", "discount_percent", "final_price_usd",
                       "units_sold", "revenue_usd", "payment_method", "sales_channel",
                       "country", "customer_income_level", "customer_rating")

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos

    orders:     lista (array_list) con todas las ventas en el orden del archivo.
    by_brand:   mapa (separate chaining) marca -> RBT con llave (descuento, fecha, order_id). Req. 1.
    by_country: mapa (separate chaining) pais  -> RBT con llave (fecha, order_id). Req. 5.
    min_sale / max_sale: venta de menor / mayor precio final (se llenan al cargar).
    """
    catalog = {
        "orders": al.new_list(),
        "by_brand": mp.new_map(16, 4),
        "by_country": mp.new_map(16, 4),
        "min_sale": None,
        "max_sale": None,
    }
    return catalog


# Utilidades

def _fecha_iso(texto):
    """
    order_date viene como AAAA-MM-DD. En ese formato comparar fechas como texto
    equivale a compararlas cronologicamente.
    """
    fecha = texto.strip()
    if len(fecha) != 10 or fecha[4] != "-" or fecha[7] != "-":
        raise ValueError("la fecha '%s' no esta en formato AAAA-MM-DD" % texto)
    return fecha


def _indexar_en_arbol(tabla, nombre, llave, orden):
    """
    Inserta la venta en el RBT asociado a 'nombre' dentro del mapa 'tabla'
    (crea el RBT si todavia no existe). La llave es una tupla unica para que
    put() nunca reemplace una venta por otra.
    """
    arbol = mp.get(tabla, nombre)
    if arbol is None:
        arbol = rbt.new_map()
        mp.put(tabla, nombre, arbol)
    rbt.put(arbol, llave, orden)


def find_data_file(name):
    """Retorna la ruta del archivo de datos (por nombre) o None si no existe."""
    if os.path.isfile(name):
        return name
    for carpeta in DATA_DIRS:
        ruta = os.path.join(carpeta, name)
        if os.path.isfile(ruta):
            return ruta
    return None


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto leyendo el CSV UNA sola vez.

    En el mismo recorrido se llena la lista principal, los indices (mapas de RBT por marca
    y por pais) y se actualizan la venta de menor y de mayor precio final.
    Si algo falla, el catalogo anterior queda intacto.

    Complejidad: O(n log n) (n inserciones en RBT de costo O(log n); put/get del mapa O(1)).
    """
    inicio = get_time()

    ruta = find_data_file(filename)
    if ruta is None:
        raise ValueError("No se encontro el archivo %s" % filename)

    nuevo = new_logic()
    ordenes = nuevo["orders"]
    menor = None
    mayor = None

    with open(ruta, encoding="utf-8-sig", newline="") as archivo_csv:
        lector = csv.reader(archivo_csv)
        encabezado = next(lector, None)
        if encabezado is None:
            raise ValueError("El archivo esta vacio: %s" % filename)

        pos = {}
        for i in range(len(encabezado)):
            pos[encabezado[i].strip()] = i
        faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in pos]
        if faltantes:
            raise ValueError("Faltan columnas en el CSV: %s" % ", ".join(faltantes))

        for fila in lector:
            if not fila:
                continue
            try:
                fecha = _fecha_iso(fila[pos["order_date"]])
                orden = {
                    "order_id": fila[pos["order_id"]].strip(),
                    "order_date": fecha,
                    "brand": fila[pos["brand"]].strip(),
                    "model_name": fila[pos["model_name"]].strip(),
                    "category": fila[pos["category"]].strip(),
                    "gender": fila[pos["gender"]].strip(),
                    "size": fila[pos["size"]].strip(),
                    "color": fila[pos["color"]].strip(),
                    "base_price_usd": float(fila[pos["base_price_usd"]]),
                    "discount_percent": float(fila[pos["discount_percent"]]),
                    "final_price_usd": float(fila[pos["final_price_usd"]]),
                    "units_sold": int(fila[pos["units_sold"]]),
                    "revenue_usd": float(fila[pos["revenue_usd"]]),
                    "payment_method": fila[pos["payment_method"]].strip(),
                    "sales_channel": fila[pos["sales_channel"]].strip(),
                    "country": fila[pos["country"]].strip(),
                    "customer_income_level": fila[pos["customer_income_level"]].strip(),
                    "customer_rating": float(fila[pos["customer_rating"]]),
                }
            except (ValueError, IndexError) as error:
                raise ValueError("Fila %d invalida: %s" % (lector.line_num, error)) from error

            al.add_last(ordenes, orden)

            # --- indices (mapa -> RBT) ---
            _indexar_en_arbol(nuevo["by_brand"], orden["brand"],
                              (orden["discount_percent"], fecha, orden["order_id"]), orden)
            _indexar_en_arbol(nuevo["by_country"], orden["country"],
                              (fecha, orden["order_id"]), orden)

            # --- menor y mayor precio final (con desempate por fecha) ---
            precio = orden["final_price_usd"]
            if (menor is None or precio < menor["final_price_usd"]
                    or (precio == menor["final_price_usd"] and fecha > menor["order_date"])):
                menor = orden          # empate: gana la mas reciente
            if (mayor is None or precio > mayor["final_price_usd"]
                    or (precio == mayor["final_price_usd"] and fecha < mayor["order_date"])):
                mayor = orden          # empate: gana la mas antigua

    nuevo["min_sale"] = menor
    nuevo["max_sale"] = mayor

    total = al.size(ordenes)
    primeros_cinco = al.new_list()
    ultimos_cinco = al.new_list()
    if total > 0:
        k = min(5, total)
        primeros_cinco = al.sub_list(ordenes, 0, k)
        ultimos_cinco = al.sub_list(ordenes, total - k, k)

    # Solo si todo salio bien se reemplaza el contenido del catalogo
    catalog.clear()
    catalog.update(nuevo)

    return {
        "total_orders": total,
        "min_order": menor,
        "max_order": mayor,
        "first_five": primeros_cinco,
        "last_five": ultimos_cinco,
        "time_ms": delta_time(inicio, get_time()),
    }

# Funciones de consulta sobre el catálogo


def req_1(catalog, brand, min_disc, max_disc):
    """
    Req. 1 (individual): ordenes de una marca con descuento en [min_disc, max_disc].

    by_brand[brand] (mapa) entrega el RBT de la marca, cuya llave es la tupla
    (descuento, fecha, order_id). rbt.values() recorre solo el rango y retorna las
    ordenes YA ordenadas: descuento ascendente y, en empate, fecha ascendente.
    Complejidad: O(1) + O(log n + k), con k las ordenes que cumplen el filtro.
    """
    inicio = get_time()

    arbol = mp.get(catalog["by_brand"], brand)

    ordenes = sll.new_list()
    costo_total = 0.0
    if arbol is not None:
        lo = (min_disc, "", "")
        hi = (max_disc, "9999-99-99", "~")
        ordenes = rbt.values(arbol, lo, hi)

        nodo = ordenes["first"]
        while nodo is not None:
            costo_total += nodo["info"]["final_price_usd"]
            nodo = nodo["next"]

    return {
        "total_orders": sll.size(ordenes),
        "total_cost": costo_total,
        "orders": ordenes,
        "time_ms": delta_time(inicio, get_time()),
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
