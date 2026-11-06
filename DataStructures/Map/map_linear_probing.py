from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
import random

def new_map(num_elements: int, load_factor: float, prime=109345121)->dict:
    """Crea una nueva tabla de hash optimizada."""
    
    capacity = int(num_elements / load_factor) + 1
    if not mf.is_prime(capacity):
        capacity = mf.next_prime(capacity)


    # Crear tabla usando array list
    tabla = al.new_list()
    i = 0
    while i < capacity:
        al.add_last(tabla, me.new_map_entry(None, None))
        i += 1

    new_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": random.randint(1, prime - 1),
        "shift": random.randint(0, prime - 1),
        "table": tabla,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
        "type": "PROBING"
    }

    return new_map

def hash_value(my_map, key)->int:
    """Función hash optimizada usando map_functions."""
    return mf.hash_value(my_map, key)

def put(my_map, key, value):
   
    # Verificar si necesitamos rehashing ANTES de insertar
    current_load = (my_map["size"] + 1) / my_map["capacity"]
    if current_load > my_map["limit_factor"]:
        my_map = rehash(my_map)

    key_hash = hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, key_hash)
    tabla = my_map["table"]
    entry = al.get_element(tabla, pos)

    if ocupied:
        # Actualizar valor existente usando map_entry functions
        me.set_value(entry, value)
    else:
        # Nueva entrada
        me.set_key(entry, key)
        me.set_value(entry, value)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map

def find_slot(my_map, key, hash_value: int)->tuple:
    
    first_avail = None
    found = False
    ocupied = False
    pos = hash_value % my_map["capacity"]

    while not found:
        if is_available(my_map["table"], pos):
            if first_avail is None:
                first_avail = pos
            entry = al.get_element(my_map["table"], pos)
            if me.get_key(entry) is None:
                found = True
        else:
            entry = al.get_element(my_map["table"], pos)
            if default_compare(key, entry) == 0:
                first_avail = pos
                found = True
                ocupied = True

        if not found:
            pos = (pos + 1) % my_map["capacity"]

    return ocupied, first_avail

def is_available(table, pos:int)->bool:
    """Verifica si la posición está disponible."""
    entry = al.get_element(table, pos)
    key = me.get_key(entry)
    if key is None or key == "__EMPTY__":
        return True
    return False

def default_compare(key, entry)->int:
    """Función de comparación usando map_entry functions."""
    entry_key = me.get_key(entry)
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1

def contains(my_map:dict, key)->bool:
    """Verifica si una llave existe."""
    key_hash = hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, key_hash)
    return ocupied

def remove(my_map:dict, key)->dict:
    """Elimina una pareja llave-valor."""
    key_hash = hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, key_hash)

    if ocupied:
        tabla = my_map["table"]
        entry = al.get_element(tabla, pos)
        me.set_key(entry, "__EMPTY__")
        me.set_value(entry, "__EMPTY__")
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map

def get(my_map:dict, key):
    """Obtiene el valor asociado a una llave."""
    key_hash = hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, key_hash)

    if ocupied:
        tabla = my_map["table"]
        entry = al.get_element(tabla, pos)
        return me.get_value(entry)

    return None

def size(my_map:dict)->int:
    """Retorna el tamaño del mapa."""
    return my_map["size"]

def is_empty(my_map)->bool:
    """Verifica si el mapa está vacío."""
    return my_map["size"] == 0

def key_set(my_map:dict):
    """Retorna array_list con todas las llaves."""
    keys = al.new_list()
    tabla = my_map["table"]

    for i in range(al.size(tabla)):
        entry = al.get_element(tabla, i)
        key = me.get_key(entry)
        if key is not None and key != "__EMPTY__":
            al.add_last(keys, key)

    return keys

def value_set(my_map:dict):
    """Retorna array_list con todos los valores."""
    values = al.new_list()
    tabla = my_map["table"]

    for i in range(al.size(tabla)):
        entry = al.get_element(tabla, i)
        key = me.get_key(entry)
        if key is not None and key != "__EMPTY__":
            al.add_last(values, me.get_value(entry))

    return values

def rehash(my_map:dict)->dict:
    
    # Guardar elementos actuales
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    # Crear nueva tabla con mayor capacidad
    new_capacity = mf.next_prime(old_capacity * 2)
    my_map["table"] = al.new_list()
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    # Inicializar nueva tabla
    for i in range(new_capacity):
        al.add_last(my_map["table"], me.new_map_entry(None, None))

    # Reinsertar elementos válidos
    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i)
        key = me.get_key(entry)
        if key is not None and key != "__EMPTY__":
            value = me.get_value(entry)
            put(my_map, key, value)

    return my_map