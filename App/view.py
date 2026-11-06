import sys

default_limit = 1000
sys.setrecursionlimit(default_limit * 10)

from tabulate import tabulate

import App.logic as logic
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll

DATA_FILES = (
    "global_sports_footwear_sales-small.csv",
    "global_sports_footwear_sales-medium.csv",
    "global_sports_footwear_sales-large.csv",
)


def new_logic():
    """
        Se crea una instancia del controlador
    """
    return logic.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def order_row(order):
    """Fila con los 10 campos que se muestran de cada venta en el reporte de carga."""
    return [order["order_id"], order["order_date"], order["brand"], order["model_name"],
            order["category"], "{:,.2f}".format(order["final_price_usd"]), order["units_sold"],
            "{:,.2f}".format(order["revenue_usd"]), order["country"], order["sales_channel"]]


def print_orders(orders):
    """Imprime una lista (array_list) de ventas con las columnas pedidas en la carga."""
    headers = ["order_id", "Fecha", "Marca", "Modelo", "Categoria", "Precio final (USD)",
               "Unidades", "Ingreso (USD)", "Pais", "Canal"]
    rows = []
    for i in range(al.size(orders)):
        rows.append(order_row(al.get_element(orders, i)))
    print(tabulate(rows, headers=headers, tablefmt="grid", disable_numparse=True))


def print_price_extreme(order):
    """Imprime una venta (menor o mayor precio final) con los 6 campos pedidos."""
    headers = ["order_id", "Marca", "Modelo", "Categoria", "Precio final (USD)", "Pais"]
    row = [order["order_id"], order["brand"], order["model_name"], order["category"],
           "{:,.2f}".format(order["final_price_usd"]), order["country"]]
    print(tabulate([row], headers=headers, tablefmt="grid", disable_numparse=True))


def print_load_report(report, filename):
    """
        Imprime el reporte de la carga de datos
    """
    print("\n=== Carga de datos: " + filename + " ===")
    print("Tiempo de carga: {:,.2f} ms".format(report["time_ms"]))
    print("Total de registros cargados: {:,}".format(report["total_orders"]))
    if report["total_orders"] == 0:
        print("El archivo no contiene ventas.\n")
        return

    print("\nVenta con menor precio final (si hay empate, la mas reciente):")
    print_price_extreme(report["min_order"])
    print("\nVenta con mayor precio final (si hay empate, la mas antigua):")
    print_price_extreme(report["max_order"])

    print("\nPrimeros 5 registros cargados:")
    print_orders(report["first_five"])
    print("\nUltimos 5 registros cargados:")
    print_orders(report["last_five"])
    print()


def load_data(control):
    """
    Carga los datos
    """
    print("Archivos disponibles:")
    for i in range(len(DATA_FILES)):
        print("  %d- %s" % (i + 1, DATA_FILES[i]))
    choice = input("Seleccione el archivo a cargar (1-%d)\n" % len(DATA_FILES)).strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(DATA_FILES):
        print("Opcion de archivo erronea.\n")
        return None

    name = DATA_FILES[int(choice) - 1]
    if logic.find_data_file(name) is None:
        print("No se encontro el archivo " + name + " en la carpeta Data.\n")
        return None

    try:
        report = logic.load_data(control, name)
    except ValueError as error:
        print("No se pudo cargar el archivo: " + str(error) + "\n")
        return None
    print_load_report(report, name)
    return report


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    if al.size(control["orders"]) == 0:
        print("Primero debe cargar la informacion (opcion 0).\n")
        return

    brand = input("Marca a analizar (ej: Nike): ").strip()
    try:
        min_disc = float(input("Descuento minimo (%): ").strip().replace(",", "."))
        max_disc = float(input("Descuento maximo (%): ").strip().replace(",", "."))
    except ValueError:
        print("Entrada invalida: los descuentos deben ser numeros.\n")
        return
    if brand == "":
        print("Entrada invalida: la marca no puede estar vacia.\n")
        return
    if min_disc > max_disc:
        print("Entrada invalida: el descuento minimo no puede ser mayor que el maximo.\n")
        return

    result = logic.req_1(control, brand, min_disc, max_disc)

    print("\n=== Requerimiento 1: %s con descuento entre %g%% y %g%% ===" % (brand, min_disc, max_disc))
    print("Tiempo de ejecucion: {:,.2f} ms".format(result["time_ms"]))
    print("Total de ordenes que cumplen el filtro: {:,}".format(result["total_orders"]))
    if result["total_orders"] == 0:
        print("No se encontraron ordenes (revise que la marca este escrita exactamente igual).\n")
        return
    print("Costo total final: {:,.2f} USD".format(result["total_cost"]))

    orders = result["orders"]
    total = sll.size(orders)
    headers = ["order_id", "Fecha", "Marca", "Modelo", "Categoria", "Pais", "Canal",
               "Descuento (%)", "Precio final (USD)"]

    def build_row(order):
        return [order["order_id"], order["order_date"], order["brand"], order["model_name"],
                order["category"], order["country"], order["sales_channel"],
                "%g" % order["discount_percent"], "{:,.2f}".format(order["final_price_usd"])]

    rows = []
    if total <= 10:
        for i in range(total):
            rows.append(build_row(sll.get_element(orders, i)))
    else:
        for i in range(5):
            rows.append(build_row(sll.get_element(orders, i)))
        for i in range(total - 5, total):
            rows.append(build_row(sll.get_element(orders, i)))

    print("\nOrdenes por descuento ascendente (y fecha ascendente en empate):")
    print(tabulate(rows, headers=headers, tablefmt="grid", disable_numparse=True))
    if total > 10:
        print("(Se muestran las 5 primeras y las 5 ultimas de {:,} ordenes)".format(total))
    print()


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
