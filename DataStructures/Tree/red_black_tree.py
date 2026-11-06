
from DataStructures.Tree import rbt_node as rbt_node
from DataStructures.List import single_linked_list as sll


def new_map():
    """
    Crea una tabla de simbolos ordenada basa en un árbol rojo-negro (RBT) vacia
    
    Returns:
        red_black_tree: La tabla de simbolos ordenada sin elementos
    """
    return {
        "root": None,
        "type": "RBT"
    }


def put(my_rbt, key, value):
    """
    Ingresa una pareja llave,valor. Si la llave ya existe, se reemplaza el valor.
    Usa la funcion insert_node()
    
    Parameters:
        my_rbt (red_black_tree): El RBT
        key (any): La llave asociada a la pareja
        value (any): El valor asociado a la pareja
    
    Returns:
        red_black_tree: El arbol con la nueva pareja
    """
    my_rbt['root'] = insert_node(my_rbt['root'], key, value)
    if my_rbt['root'] is not None:
        my_rbt['root']['color'] = 1  # La raíz siempre debe ser negra (1 = negro)
    return my_rbt


def insert_node(root, key, value):
    """
    Ingresa una pareja llave,valor. Si la llave ya existe, se reemplaza el valor.
    Es usada en la función put()
    
    Parameters:
        root (rbt_node): La raiz del arbol
        key (any): La llave asociada a la pareja
        value (any): El valor asociado a la pareja
    
    Returns:
        rbt_node: El arbol con la nueva pareja
    """
    if root is None:
        return rbt_node.new_node(key, value, 0)  # 0 = rojo
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        root['left'] = insert_node(root['left'], key, value)
    elif cmp > 0:
        root['right'] = insert_node(root['right'], key, value)
    else:
        root['value'] = value
    
    if is_red(root['right']) and not is_red(root['left']):
        root = rotate_left(root)
    
    if is_red(root['left']) and root['left'] is not None and is_red(root['left']['left']):
        root = rotate_right(root)
    
    if is_red(root['left']) and is_red(root['right']):
        flip_colors(root)
    
    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    
    return root


def get(my_rbt, key):
    """
    Retorna el valor con llave igual a key
    Usa la función get_node() para buscar la llave en el arbol
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): La llave asociada a la pareja
    
    Returns:
        any: El valor de la llave key. None en caso de no ser encontrada
    """
    return get_node(my_rbt['root'], key)


def get_node(root, key):
    """
    Retorna el valor de la llave igual a key
    
    Parameters:
        root (rbt_node): La raiz del arbol
        key (any): La llave asociada a la pareja a buscar
    
    Returns:
        any: El valor de la llave key. None en caso de no ser encontrada
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        return get_node(root['left'], key)
    elif cmp > 0:
        return get_node(root['right'], key)
    else:
        return rbt_node.get_value(root)


def remove(my_rbt, key):
    """
    Elimina la pareja llave-valor que coincida con key.
    Usa la función remove_node() para eliminar la pareja
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): La llave asociada a la pareja a eliminar
    
    Returns:
        red_black_tree: El arbol sin la pareja key-value
    """
    if not contains(my_rbt, key):
        return my_rbt
    
    if not is_red(my_rbt['root']['left']) and not is_red(my_rbt['root']['right']):
        my_rbt['root']['color'] = 0  # rojo
    
    my_rbt['root'] = remove_node(my_rbt['root'], key)
    
    if not is_empty(my_rbt):
        my_rbt['root']['color'] = 1  # negro
    
    return my_rbt


def remove_node(root, key):
    """
    Elimina la pareja llave-valor que coincida con key.
    Es usada en la función remove()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key (any): La llave asociada a la pareja a eliminar
    
    Returns:
        rbt_node: El arbol sin la pareja key-value
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        if root['left'] is not None:
            if not is_red(root['left']) and not is_red(root['left']['left']):
                root = move_red_left(root)
        root['left'] = remove_node(root['left'], key)
    else:
        if is_red(root['left']):
            root = rotate_right(root)
        
        cmp = default_compare(key, root)
        if cmp == 0 and root['right'] is None:
            return None
        
        if root['right'] is not None:
            if not is_red(root['right']) and not is_red(root['right']['left']):
                root = move_red_right(root)
        
        cmp = default_compare(key, root)
        if cmp == 0:
            min_node = get_min_node(root['right'])
            root['key'] = min_node['key']
            root['value'] = min_node['value']
            root['right'] = delete_min_node(root['right'])
        else:
            root['right'] = remove_node(root['right'], key)
    
    return balance(root)


def contains(my_rbt, key):
    """
    Informa si la llave key se encuentra en la tabla de hash.
    Usa la función get() para buscar la llave en el arbol
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): La llave a buscar
    
    Returns:
        bool: True si la llave está presente, False en caso contrario
    """
    return get(my_rbt, key) is not None


def size(my_rbt):
    """
    Retorna el número de entradas en la tabla de simbolos
    Usa la función size_tree() para contar el número de elementos
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        int: El número de elementos en la tabla
    """
    return size_tree(my_rbt['root'])


def is_empty(my_rbt):
    """
    Informa si la tabla de simbolos se encuentra vacia.
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        bool: True si la tabla es vacía, False en caso contrario
    """
    return my_rbt['root'] is None


def key_set(my_rbt):
    """
    Retorna una lista con todas las llaves de la tabla.
    Usa la función key_set_tree() para construir la lista de llaves
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        single_linked_list: Una lista con todas las llaves de la tabla
    """
    key_list = sll.new_list()
    return key_set_tree(my_rbt['root'], key_list)


def key_set_tree(root, key_list):
    """
    Construye una lista con las llaves de la tabla. Se recorre el arbol en inorder
    Es usada en la función key_set()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key_list (single_linked_list): La lista de respuesta
    
    Returns:
        single_linked_list: Una lista con todos las llaves
    """
    if root is not None:
        key_set_tree(root['left'], key_list)
        sll.add_last(key_list, rbt_node.get_key(root))
        key_set_tree(root['right'], key_list)
    return key_list


def value_set(my_rbt):
    """
    Retorna una lista con los valores de la tabla.
    Usa la función value_set_tree() para construir la lista de valores
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        single_linked_list: Una lista con todos los valores de la tabla
    """
    value_list = sll.new_list()
    return value_set_tree(my_rbt['root'], value_list)


def value_set_tree(root, value_list):
    """
    Construye una lista con los valores de la tabla. Se recorre el arbol en inorder
    Es usada en la función value_set()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        value_list (single_linked_list): La lista de respuesta
    
    Returns:
        single_linked_list: Una lista con todos los valores
    """
    if root is not None:
        value_set_tree(root['left'], value_list)
        sll.add_last(value_list, rbt_node.get_value(root))
        value_set_tree(root['right'], value_list)
    return value_list


def get_min(my_rbt):
    """
    Retorna la llave mas a la izquierda de la tabla de simbolos
    Usa la función get_min_node() para encontrar la llave más a la izquierda
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        any: La llave más a la izquierda
    """
    if my_rbt['root'] is None:
        return None
    return rbt_node.get_key(get_min_node(my_rbt['root']))


def get_min_node(root):
    """
    Retorna el nodo con la llave mas a la izquierda de la tabla de simbolos
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        rbt_node: El nodo más a la izquierda
    """
    if root['left'] is None:
        return root
    return get_min_node(root['left'])


def get_max(my_rbt):
    """
    Retorna la llave mas a la derecha de la tabla de simbolos
    Usa la función get_max_node() para encontrar la llave más a la derecha
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        any: La llave más a la derecha
    """
    if my_rbt['root'] is None:
        return None
    return rbt_node.get_key(get_max_node(my_rbt['root']))


def get_max_node(root):
    """
    Retorna el nodo con la llave mas a la derecha de la tabla de simbolos
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        rbt_node: El nodo más a la derecha
    """
    if root['right'] is None:
        return root
    return get_max_node(root['right'])


def delete_min(my_rbt):
    """
    Encuentra y remueve la llave mas a la izquierda de la tabla de simbolos 
    y su valor asociado.
    Usa la función delete_min_node() para eliminar la llave más a la izquierda
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        red_black_tree: El arbol de búsqueda sin la llave más a la izquierda
    """
    if is_empty(my_rbt):
        return my_rbt
    
    if not is_red(my_rbt['root']['left']) and not is_red(my_rbt['root']['right']):
        my_rbt['root']['color'] = 0  # rojo
    
    my_rbt['root'] = delete_min_node(my_rbt['root'])
    
    if not is_empty(my_rbt):
        my_rbt['root']['color'] = 1  # negro
    
    return my_rbt


def delete_min_node(root):
    """
    Encuentra y remueve la llave mas a la izquierda de la tabla de simbolos 
    y su valor asociado
    Es usada en la función delete_min()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        rbt_node: Retorna la raiz del arbol sin la llave más a la izquierda
    """
    if root['left'] is None:
        return None
    
    if not is_red(root['left']) and not is_red(root['left']['left']):
        root = move_red_left(root)
    
    root['left'] = delete_min_node(root['left'])
    
    return balance(root)


def delete_max(my_rbt):
    """
    Encuentra y remueve la llave mas a la derecha de la tabla de simbolos 
    y su valor asociado.
    Usa la función delete_max_node() para eliminar la llave más a la derecha
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        red_black_tree: El arbol de búsqueda sin la llave más a la derecha
    """
    if is_empty(my_rbt):
        return my_rbt
    
    if not is_red(my_rbt['root']['left']) and not is_red(my_rbt['root']['right']):
        my_rbt['root']['color'] = 0  # rojo
    
    my_rbt['root'] = delete_max_node(my_rbt['root'])
    
    if not is_empty(my_rbt):
        my_rbt['root']['color'] = 1  # negro
    
    return my_rbt


def delete_max_node(root):
    """
    Encuentra y remueve la llave mas a la derecha de la tabla de simbolos 
    y su valor asociado.
    Es usada en la función delete_max()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        rbt_node: Retorna la raiz del arbol sin la llave más a la derecha
    """
    if is_red(root['left']):
        root = rotate_right(root)
    
    if root['right'] is None:
        return None
    
    if not is_red(root['right']) and not is_red(root['right']['left']):
        root = move_red_right(root)
    
    root['right'] = delete_max_node(root['right'])
    
    return balance(root)


def floor(my_rbt, key):
    """
    Retorna la llave que precede a la llave key en la tabla de simbolos.
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): La llave de búsqueda
    
    Returns:
        any: La llave predecesora a key
    """
    if is_empty(my_rbt):
        return None
    
    floor_node = floor_key(my_rbt['root'], key)
    if floor_node is None:
        return None
    return rbt_node.get_key(floor_node)


def floor_key(root, key):
    """
    Retorna el nodo con la llave que precede a la llave key.
    Es usada en la función floor()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key (any): La llave de búsqueda
    
    Returns:
        rbt_node: El nodo con la llave predecesora a key
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp < 0:
        return floor_key(root['left'], key)
    
    temp = floor_key(root['right'], key)
    if temp is not None:
        return temp
    
    return root


def ceiling(my_rbt, key):
    """
    Retorna la llave que sucede a la llave key en la tabla de simbolos.
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): La llave de búsqueda
    
    Returns:
        any: La llave sucesora a key
    """
    if is_empty(my_rbt):
        return None
    
    ceiling_node = ceiling_key(my_rbt['root'], key)
    if ceiling_node is None:
        return None
    return rbt_node.get_key(ceiling_node)


def ceiling_key(root, key):
    """
    Retorna el nodo con la llave que sucede a la llave key.
    Es usada en la función ceiling()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key (any): La llave de búsqueda
    
    Returns:
        rbt_node: El nodo con la llave sucesora a key
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp > 0:
        return ceiling_key(root['right'], key)
    
    temp = ceiling_key(root['left'], key)
    if temp is not None:
        return temp
    
    return root


def select(my_rbt, pos):
    """
    Retorna la siguiente llave a la k-esima llave de izquierda a derecha 
    de la tabla de simbolos.
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        pos (int): la pos-esima llave de izquierda a derecha
    
    Returns:
        any: La llave en la posición pos
    """
    if is_empty(my_rbt) or pos < 0 or pos >= size(my_rbt):
        return None
    
    node = select_key(my_rbt['root'], pos)
    return rbt_node.get_key(node)


def select_key(root, pos):
    """
    Retorna el nodo con la k-esima llave de izquierda a derecha.
    Es usada en la función select()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        pos (int): la posición de búsqueda
    
    Returns:
        rbt_node: El nodo en la posición pos
    """
    if root is None:
        return None
    
    left_size = size_tree(root['left'])
    
    if left_size > pos:
        return select_key(root['left'], pos)
    elif left_size < pos:
        return select_key(root['right'], pos - left_size - 1)
    else:
        return root


def rank(my_rbt, key):
    """
    Retorna el número de llaves en la tabla que son estrictamente predecesoras a key
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
        key (any): la llave de busqueda
    
    Returns:
        int: El número de llaves
    """
    return rank_keys(my_rbt['root'], key)


def rank_keys(root, key):
    """
    Retorna el número de llaves en la tabla que son estrictamente predecesoras a key
    Es usada en la función rank()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key (any): la llave de busqueda
    
    Returns:
        int: El número de llaves
    """
    if root is None:
        return 0
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        return rank_keys(root['left'], key)
    elif cmp > 0:
        return 1 + size_tree(root['left']) + rank_keys(root['right'], key)
    else:
        return size_tree(root['left'])


def height(my_rbt):
    """
    Retorna la altura del arbol de busqueda
    Usa la función height_tree() para encontrar la altura del arbol
    
    Parameters:
        my_rbt (red_black_tree): El arbol de búsqueda
    
    Returns:
        int: La altura del arbol
    """
    return height_tree(my_rbt['root'])


def height_tree(root):
    """
    Retorna la altura del arbol de busqueda
    Es usada en la función height()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        int: La altura del arbol
    """
    if root is None:
        return -1
    
    left_height = height_tree(root['left'])
    right_height = height_tree(root['right'])
    
    return 1 + max(left_height, right_height)


def keys(my_rbt, key_initial, key_final):
    """
    Retorna todas las llaves del arbol que se encuentren entre [key_initial, key_final].
    Usa la función keys_range() para encontrar las llaves en el rango especificado
    
    Parameters:
        my_rbt (red_black_tree): La tabla de simbolos
        key_initial (any): limite inferior
        key_final (any): limite superior
    
    Returns:
        single_linked_list: Las llaves en el rango especificado
    """
    key_list = sll.new_list()
    return keys_range(my_rbt['root'], key_initial, key_final, key_list)


def keys_range(root, key_initial, key_final, list_key):
    """
    Retorna todas las llaves del arbol que se encuentren entre [key_initial, key_final].
    Es usada en la función keys()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key_initial (any): limite inferior
        key_final (any): limite superior
        list_key (single_linked_list): La lista de respuesta
    
    Returns:
        single_linked_list: Las llaves en el rango especificado
    """
    if root is None:
        return list_key
    
    cmp_lo = default_compare(key_initial, root)
    cmp_hi = default_compare(key_final, root)
    
    if cmp_lo < 0:
        keys_range(root['left'], key_initial, key_final, list_key)
    
    if cmp_lo <= 0 and cmp_hi >= 0:
        sll.add_last(list_key, rbt_node.get_key(root))
    
    if cmp_hi > 0:
        keys_range(root['right'], key_initial, key_final, list_key)
    
    return list_key


def values(my_rbt, key_initial, key_final):
    """
    Retorna todas los valores del arbol que se encuentren entre [key_initial, key_final]
    Usa la función values_range() para encontrar los valores en el rango especificado
    
    Parameters:
        my_rbt (red_black_tree): La tabla de simbolos
        key_initial (any): limite inferior
        key_final (any): limite superior
    
    Returns:
        single_linked_list: Los valores en el rango especificado
    """
    value_list = sll.new_list()
    return values_range(my_rbt['root'], key_initial, key_final, value_list)


def values_range(root, key_initial, key_final, value_list):
    """
    Retorna todas los valores del arbol que se encuentren entre [key_initial, key_final]
    Es usada en la función values()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
        key_initial (any): limite inferior
        key_final (any): limite superior
        value_list (single_linked_list): La lista de respuesta
    
    Returns:
        single_linked_list: Los valores en el rango especificado
    """
    if root is None:
        return value_list
    
    cmp_lo = default_compare(key_initial, root)
    cmp_hi = default_compare(key_final, root)
    
    if cmp_lo < 0:
        values_range(root['left'], key_initial, key_final, value_list)
    
    if cmp_lo <= 0 and cmp_hi >= 0:
        sll.add_last(value_list, rbt_node.get_value(root))
    
    if cmp_hi > 0:
        values_range(root['right'], key_initial, key_final, value_list)
    
    return value_list


# ============================================================================
# Funciones auxiliares y de soporte
# ============================================================================

def default_compare(key, element):
    """
    Función de comparación por defecto. 
    Compara una llave con la llave de un elemento llave-valor.
    
    Parameters:
        key (any): Llave a comparar
        element (rbt_node): entry a comparar
    
    Returns:
        int: 0 si son iguales, 1 si key > la llave del element, 
             -1 si key < que la llave del element
    """
    element_key = rbt_node.get_key(element)
    
    if key == element_key:
        return 0
    elif key > element_key:
        return 1
    else:
        return -1


def is_red(node_rbt):
    """
    Indica si un nodo del arbol es rojo
    
    Parameters:
        node_rbt (rbt_node): El nodo a examinar
    
    Returns:
        bool: True si el nodo es rojo, False de lo contrario
    """
    if node_rbt is None:
        return False
    return rbt_node.is_red(node_rbt)


def size_tree(root):
    """
    Retornar el número de entradas en la a partir del nodo root
    Es usada en la función size()
    
    Parameters:
        root (rbt_node): La raiz del arbol a examinar
    
    Returns:
        int: El número de elementos en la tabla
    """
    if root is None:
        return 0
    return root['size']


def rotate_left(node_rbt):
    """
    Rotación izquierda para compensar dos enlaces rojos consecutivos
    
    Parameters:
        node_rbt (rbt_node): Nodo raiz del arbol a rotar
    
    Returns:
        rbt_node: El arbol rotado
    """
    x = node_rbt['right']
    node_rbt['right'] = x['left']
    x['left'] = node_rbt
    x['color'] = node_rbt['color']
    node_rbt['color'] = 0  # rojo
    x['size'] = node_rbt['size']
    node_rbt['size'] = 1 + size_tree(node_rbt['left']) + size_tree(node_rbt['right'])
    return x


def rotate_right(node_rbt):
    """
    Rotación a la derecha para compensar un hijo rojo a la derecha
    
    Parameters:
        node_rbt (rbt_node): Nodo raiz del arbol a rotar
    
    Returns:
        rbt_node: El arbol rotado
    """
    x = node_rbt['left']
    node_rbt['left'] = x['right']
    x['right'] = node_rbt
    x['color'] = node_rbt['color']
    node_rbt['color'] = 0  # rojo
    x['size'] = node_rbt['size']
    node_rbt['size'] = 1 + size_tree(node_rbt['left']) + size_tree(node_rbt['right'])
    return x


def flip_colors(node_rbt):
    """
    Cambia el color de un nodo y de sus dos hijos
    
    Parameters:
        node_rbt (rbt_node): El nodo a cambiar
    
    Returns:
        rbt_node: El nodo con el color opuesto
    """
    node_rbt['color'] = 1 - node_rbt['color']
    if node_rbt['left'] is not None:
        node_rbt['left']['color'] = 1 - node_rbt['left']['color']
    if node_rbt['right'] is not None:
        node_rbt['right']['color'] = 1 - node_rbt['right']['color']
    return node_rbt


def flip_node_color(node_rbt):
    """
    Cambia el color de un nodo
    
    Parameters:
        node_rbt (rbt_node): El nodo a cambiar
    
    Returns:
        rbt_node: El nodo con el color opuesto
    """
    if node_rbt is not None:
        node_rbt['color'] = 1 - node_rbt['color']
    return node_rbt


def move_red_left(root):
    """
    Cambio de color durante el proceso de eliminacion
    
    Parameters:
        root (rbt_node): Raiz del arbol
    
    Returns:
        rbt_node: El arbol con el hijo izquierdo de root en negro
    """
    flip_colors(root)
    if root['right'] is not None and is_red(root['right']['left']):
        root['right'] = rotate_right(root['right'])
        root = rotate_left(root)
        flip_colors(root)
    return root


def move_red_right(root):
    """
    Cambio de color durante el proceso de eliminacion
    
    Parameters:
        root (rbt_node): Raiz del arbol
    
    Returns:
        rbt_node: El arbol con un hijo derecho de root en negro
    """
    flip_colors(root)
    if root['left'] is not None and is_red(root['left']['left']):
        root = rotate_right(root)
        flip_colors(root)
    return root


def balance(root):
    """
    Balancea el arbol
    
    Parameters:
        root (rbt_node): raiz del arbol
    
    Returns:
        rbt_node: Raiz con el arbol balanceado
    """
    if is_red(root['right']) and not is_red(root['left']):
        root = rotate_left(root)
    
    if is_red(root['left']) and root['left'] is not None and is_red(root['left']['left']):
        root = rotate_right(root)
    
    if is_red(root['left']) and is_red(root['right']):
        flip_colors(root)
    
    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    
    return root
