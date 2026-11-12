import csv
import os
import time
import math

from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_separate_chaining as mp
from DataStructures.Tree import red_black_tree as rbt

# Evita problemas de buffer al leer el CSV (recomendado en el enunciado)
csv.field_size_limit(2147483647)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIRS = (os.path.join(BASE_DIR, "..", "Data", "Data"), os.path.join(BASE_DIR, "..", "Data"))

COLUMNAS_REQUERIDAS = ("order_id", "order_date", "brand", "model_name", "category", "gender",
                       "size", "color", "base_price_usd", "discount_percent", "final_price_usd",
                       "units_sold", "revenue_usd", "payment_method", "sales_channel",
                       "country", "customer_income_level", "customer_rating")

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "orders": al.new_list(),
        "by_brand": mp.new_map(16, 4),
        "by_country": mp.new_map(16, 4),
        "by_country_rating": mp.new_map(16, 4),
        "by_brand_income": mp.new_map(16, 4),
        "by_brand_date": mp.new_map(16, 4),
        "min_sale": None,
        "max_sale": None,
    }
    return catalog


# Utilidades

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
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    inicio = get_time()
 
    ruta = find_data_file(filename)
    if ruta is None:
        return None
 
    nuevo = new_logic()
    ordenes = nuevo["orders"]
    menor = None
    mayor = None
 
    with open(ruta, encoding="utf-8-sig", newline="") as archivo_csv:
        lector = csv.reader(archivo_csv)
        encabezado = next(lector, None)
        if encabezado is None:
            return None
 
        pos = {}
        for i in range(len(encabezado)):
            pos[encabezado[i].strip()] = i
        faltantes = []
        for c in COLUMNAS_REQUERIDAS:
            if c not in pos:
                faltantes.append(c)
        if faltantes:
            return None
 
        for fila in lector:
            if not fila:
                continue
            fecha = fila[pos["order_date"]].strip()
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
 
            al.add_last(ordenes, orden)
 
            _indexar_en_arbol(nuevo["by_brand"], orden["brand"],
                              (orden["discount_percent"], fecha, orden["order_id"]), orden)
            _indexar_en_arbol(nuevo["by_country"], orden["country"],
                              (fecha, orden["order_id"]), orden)
            _indexar_en_arbol(nuevo["by_country_rating"], orden["country"],
                              (orden["customer_rating"], fecha, orden["order_id"]), orden)       
            _indexar_en_arbol(nuevo["by_brand_income"], orden["brand"],
                              (orden["customer_income_level"], fecha, orden["order_id"]), orden)  
            _indexar_en_arbol(nuevo["by_brand_date"], orden["brand"],
                              (fecha, orden["order_id"]), orden)                                 
 
            precio = orden["final_price_usd"]
            if (menor is None or precio < menor["final_price_usd"]
                    or (precio == menor["final_price_usd"] and fecha > menor["order_date"])):
                menor = orden
            if (mayor is None or precio > mayor["final_price_usd"]
                    or (precio == mayor["final_price_usd"] and fecha < mayor["order_date"])):
                mayor = orden
 
    nuevo["min_sale"] = menor
    nuevo["max_sale"] = mayor
 
    total = al.size(ordenes)
    primeros_cinco = al.new_list()
    ultimos_cinco = al.new_list()
    if total > 0:
        k = min(5, total)
        primeros_cinco = al.sub_list(ordenes, 0, k)
        ultimos_cinco = al.sub_list(ordenes, total - k, k)
 
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


def req_1(catalog, brand, min_disc, max_disc):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
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


def req_2(catalog, country, min_rating, max_rating):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    inicio = get_time()

    arbol = mp.get(catalog["by_country_rating"], country)

    mostrar = sll.new_list()
    total = 0
    costo_total = 0.0
    if arbol is not None:
        lo = (min_rating, "", "")
        hi = (max_rating, "9999-99-99", "~")
        ordenes = rbt.values(arbol, lo, hi)
        total = sll.size(ordenes)

        posicion = 0
        nodo = ordenes["first"]
        while nodo is not None:
            orden = nodo["info"]
            costo_total += orden["final_price_usd"]
            if posicion < 5 or posicion >= total - 5:
                sll.add_first(mostrar, orden)
            posicion += 1
            nodo = nodo["next"]

    return {
        "total_orders": total,
        "total_cost": costo_total,
        "orders": mostrar,
        "time_ms": delta_time(inicio, get_time()),
    }


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog, start_date, end_date, income_level, n):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    inicio = get_time()

    por_marca = catalog["by_brand_income"]
    ranking = rbt.new_map()

    marcas = mp.key_set(por_marca)
    for i in range(al.size(marcas)):
        marca = al.get_element(marcas, i)
        arbol = mp.get(por_marca, marca)

        ordenes = rbt.values(arbol, (income_level, start_date, ""), (income_level, end_date, "~"))
        cantidad = sll.size(ordenes)
        if cantidad == 0:
            continue

        suma_precio = 0.0
        suma_ingreso = 0.0
        mejor = None
        nodo = ordenes["first"]
        while nodo is not None:
            orden = nodo["info"]
            suma_precio += orden["final_price_usd"]
            ingreso = orden["revenue_usd"]
            suma_ingreso += ingreso
            if mejor is None or ingreso >= mejor["revenue_usd"]:
                mejor = orden
            nodo = nodo["next"]

        rbt.put(ranking, (-cantidad, marca), {
            "brand": marca,
            "total_orders": cantidad,
            "avg_price": suma_precio / cantidad,
            "avg_revenue": suma_ingreso / cantidad,
            "best_order": mejor,
        })

    elegidas = sll.new_list()
    ordenadas = rbt.value_set(ranking)
    nodo = ordenadas["first"]
    tomadas = 0
    while nodo is not None and tomadas < n:
        sll.add_last(elegidas, nodo["info"])
        tomadas += 1
        nodo = nodo["next"]

    return {
        "total_brands": rbt.size(ranking),
        "brands": elegidas,
        "time_ms": delta_time(inicio, get_time()),
    }

  


def req_5(catalog, country, date_from, date_to, n):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    inicio = get_time()

    arbol = mp.get(catalog["by_country"], country)

    por_marca = mp.new_map(16, 4)
    total_ordenes = 0
    if arbol is not None:
        ordenes = rbt.values(arbol, (date_from, ""), (date_to, "~"))
        nodo = ordenes["first"]
        while nodo is not None:
            orden = nodo["info"]
            acc = mp.get(por_marca, orden["brand"])
            if acc is None:
                acc = {"brand": orden["brand"], "orders": 0, "sum_rating": 0.0,
                       "sum_revenue": 0.0, "best_order": orden}
                mp.put(por_marca, orden["brand"], acc)
            acc["orders"] += 1
            acc["sum_rating"] += orden["customer_rating"]
            acc["sum_revenue"] += orden["revenue_usd"]
            mejor = acc["best_order"]
            if (orden["units_sold"] > mejor["units_sold"]
                    or (orden["units_sold"] == mejor["units_sold"]
                        and orden["order_id"] > mejor["order_id"])):
                acc["best_order"] = orden
            total_ordenes += 1
            nodo = nodo["next"]

    ranking = rbt.new_map()
    marcas = mp.value_set(por_marca)
    for i in range(al.size(marcas)):
        acc = al.get_element(marcas, i)
        acc["avg_rating"] = acc["sum_rating"] / acc["orders"]
        acc["avg_revenue"] = acc["sum_revenue"] / acc["orders"]
        rbt.put(ranking, (-acc["avg_rating"], acc["brand"]), acc)

    top = al.new_list()
    nodo = rbt.value_set(ranking)["first"]
    while nodo is not None and al.size(top) < n:
        al.add_last(top, nodo["info"])
        nodo = nodo["next"]

    return {
        "total_orders": total_ordenes,
        "total_brands": mp.size(por_marca),
        "top": top,
        "time_ms": delta_time(inicio, get_time()),
    }


def req_6(catalog, start_date, end_date, min_price, max_price, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    inicio = get_time()

    por_marca = catalog["by_brand_date"]
    ranking = rbt.new_map()

    marcas = mp.key_set(por_marca)
    for i in range(al.size(marcas)):
        marca = al.get_element(marcas, i)
        arbol = mp.get(por_marca, marca)

        ordenes = rbt.values(arbol, (start_date, ""), (end_date, "~"))

        cantidad = 0
        suma = 0.0
        nodo = ordenes["first"]
        while nodo is not None:
            orden = nodo["info"]
            precio_base = orden["base_price_usd"]
            if min_price <= precio_base <= max_price:
                cantidad += 1
                suma += orden["discount_percent"]
            nodo = nodo["next"]
        if cantidad == 0:
            continue
        promedio = suma / cantidad

        suma_cuadrados = 0.0
        cercana = None
        menor_dif = 0.0
        nodo = ordenes["first"]
        while nodo is not None:
            orden = nodo["info"]
            precio_base = orden["base_price_usd"]
            if min_price <= precio_base <= max_price:
                dif = orden["discount_percent"] - promedio
                suma_cuadrados += dif * dif
                if dif < 0:
                    dif = -dif
                if (cercana is None or dif < menor_dif
                        or (dif == menor_dif and orden["order_id"] < cercana["order_id"])):
                    cercana = orden
                    menor_dif = dif
            nodo = nodo["next"]
        desviacion = math.sqrt(suma_cuadrados / cantidad)

        rbt.put(ranking, (round(desviacion, 9), promedio, marca), {
            "brand": marca,
            "total_orders": cantidad,
            "avg_discount": promedio,
            "std_discount": desviacion,
            "closest_order": cercana,
        })

    elegidas = sll.new_list()
    ordenadas = rbt.value_set(ranking)
    nodo = ordenadas["first"]
    tomadas = 0
    while nodo is not None and tomadas < n:
        sll.add_last(elegidas, nodo["info"])
        tomadas += 1
        nodo = nodo["next"]

    return {
        "total_brands": rbt.size(ranking),
        "brands": elegidas,
        "time_ms": delta_time(inicio, get_time()),
    }


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
