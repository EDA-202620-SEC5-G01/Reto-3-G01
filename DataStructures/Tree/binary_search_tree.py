from DataStructures.Tree import bst_node as bn
from DataStructures.List import single_linked_list as sl


def new_map():
    """
    Crea una nueva tabla de simbolos (map) ordenada basada en un árbol binario de búsqueda (BST).
    
    Returns:
        binary_search_tree: tabla de simbolos creada
    """
    return {"root": None}


def put(my_bst, key, value):
    """
    Agrega un nuevo nodo llave-valor a un árbol binario de búsqueda (BST). 
    Si la llave ya existe, se actualiza el value del nodo.
    
    Args:
        my_bst (binary_search_tree): árbol binario de búsqueda donde se quiere agregar el nodo
        key (any): llave del nodo
        value (any): valor del nodo
    
    Returns:
        binary_search_tree: árbol binario de búsqueda actualizado
    """
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst


def insert_node(root, key, value):
    """
    Inserta un nuevo nodo llave-valor en el árbol binario de búsqueda (BST) de manera recursiva.
    
    Args:
        root (bst_node): raiz del árbol donde se quiere agregar el nodo
        key (any): llave del nodo
        value (any): valor del nodo
    
    Returns:
        bst_node: raiz del árbol binario de búsqueda actualizado
    """
    if root is None:
        return bn.new_node(key, value)
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        # La llave ya existe, actualizar el valor
        root["value"] = value
    
    # Actualizar el tamaño del subárbol
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root


def get(my_bst, key):
    """
    Busca un nodo en el árbol binario de búsqueda (BST) y devuelve su valor.
    
    Args:
        my_bst (binary_search_tree): árbol binario de búsqueda donde se quiere buscar el nodo
        key (any): llave del nodo a buscar
    
    Returns:
        any: valor del nodo encontrado o None si no se encuentra
    """
    nodo = get_node(my_bst["root"], key)
    if nodo is not None:
        return bn.get_value(nodo)
    return None


def get_node(root, key):
    """
    Busca un nodo en el árbol binario de búsqueda (BST) de manera recursiva.
    
    Args:
        root (bst_node): raiz del árbol donde se quiere buscar el nodo
        key (any): llave del nodo a buscar
    
    Returns:
        bst_node: nodo encontrado o None si no se encuentra
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    elif cmp < 0:
        return get_node(root["left"], key)
    else:
        return get_node(root["right"], key)


def remove(my_bst, key):
    """
    Elimina la pareja llave-valor que coincida con key.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key (any): llave del nodo a buscar
    
    Returns:
        binary_search_tree: El arbol sin la pareja key-value
    """
    if not contains(my_bst, key):
        return my_bst
    
    my_bst["root"] = remove_node(my_bst["root"], key)
    return my_bst


def remove_node(root, key):
    """
    Elimina la pareja llave-valor que coincida con key.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key (any): La llave asociada a la pareja a eliminar
    
    Returns:
        bst_node: El arbol sin la pareja key-value
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        root["left"] = remove_node(root["left"], key)
    elif cmp > 0:
        root["right"] = remove_node(root["right"], key)
    else:
        # Caso 1: sin hijos
        if root["left"] is None and root["right"] is None:
            return None
        
        # Caso 2: un solo hijo
        if root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        
        # Caso 3: dos hijos
        # Buscar el sucesor (mínimo del subárbol derecho)
        sucesor = get_min_node(root["right"])
        root["key"] = sucesor["key"]
        root["value"] = sucesor["value"]
        root["right"] = remove_node(root["right"], sucesor["key"])
    
    # Actualizar tamaño
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root


def contains(my_bst, key):
    """
    Informa si la llave key se encuentra en la tabla de hash.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key (any): La llave a buscar
    
    Returns:
        bool: True si la llave está presente, False en caso contrario
    """
    return get(my_bst, key) is not None


def size(my_bst):
    """
    Retorna el número de entradas en la tabla de simbolos
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        int: El número de elementos en la tabla
    """
    return size_tree(my_bst["root"])


def size_tree(root):
    """
    Retornar el número de entradas en la a partir del nodo root
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        int: El número de elementos en la tabla
    """
    if root is None:
        return 0
    
    if "size" in root:
        return root["size"]
    
    return 1 + size_tree(root["left"]) + size_tree(root["right"])


def is_empty(my_bst):
    """
    Informa si la tabla de simbolos se encuentra vacia.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        bool: True si la tabla es vacía, False en caso contrario
    """
    return my_bst["root"] is None


def key_set(my_bst):
    """
    Retorna una lista con todas las llaves de la tabla.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        single_linked_list: Una lista con todas las llaves de la tabla
    """
    lista = sl.new_list()
    key_set_tree(my_bst["root"], lista)
    return lista


def key_set_tree(root, key_list):
    """
    Construye una lista con las llaves de la tabla. Se recorre el arbol en inorder.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key_list (single_linked_list): La lista donde se agregan las llaves
    
    Returns:
        single_linked_list: Una lista con todas las llaves de la tabla
    """
    if root is not None:
        # Recorrido in-order: izquierda → raíz → derecha
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, root["key"])
        key_set_tree(root["right"], key_list)
    
    return key_list


def value_set(my_bst):
    """
    Retorna una lista con todos los valores del árbol en orden.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        single_linked_list: Una lista con todos los valores
    """
    lista = sl.new_list()
    value_set_tree(my_bst["root"], lista)
    return lista


def value_set_tree(root, value_list):
    """
    Recorre el árbol in-order y agrega los valores a la lista.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        value_list (single_linked_list): La lista donde se agregan los valores
    
    Returns:
        single_linked_list: Una lista con todos los valores
    """
    if root is not None:
        value_set_tree(root["left"], value_list)
        sl.add_last(value_list, root["value"])
        value_set_tree(root["right"], value_list)
    
    return value_list


def get_min(my_bst):
    """
    Retorna la llave mínima del árbol.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        any: La llave mínima, o None si el árbol está vacío
    """
    if is_empty(my_bst):
        return None
    
    nodo = get_min_node(my_bst["root"])
    return bn.get_key(nodo)


def get_min_node(root):
    """
    Retorna el nodo con la llave mínima.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        bst_node: El nodo con la llave mínima
    """
    if root is None:
        return None
    
    if root["left"] is None:
        return root
    
    return get_min_node(root["left"])


def get_max(my_bst):
    """
    Retorna la llave máxima del árbol.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        any: La llave máxima, o None si el árbol está vacío
    """
    if is_empty(my_bst):
        return None
    
    nodo = get_max_node(my_bst["root"])
    return bn.get_key(nodo)


def get_max_node(root):
    """
    Retorna el nodo con la llave máxima.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        bst_node: El nodo con la llave máxima
    """
    if root is None:
        return None
    
    if root["right"] is None:
        return root
    
    return get_max_node(root["right"])


def delete_min(my_bst):
    """
    Elimina el nodo con la llave mínima del árbol.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        binary_search_tree: El arbol sin el nodo mínimo
    """
    if is_empty(my_bst):
        return my_bst
    
    my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst


def delete_min_tree(root):
    """
    Elimina el nodo mínimo recursivamente.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        bst_node: La nueva raiz del subárbol
    """
    if root is None:
        return None
    
    if root["left"] is None:
        return root["right"]
    
    root["left"] = delete_min_tree(root["left"])
    
    # Actualizar tamaño
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root


def delete_max(my_bst):
    """
    Elimina el nodo con la llave máxima del árbol.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        binary_search_tree: El arbol sin el nodo máximo
    """
    if is_empty(my_bst):
        return my_bst
    
    my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst


def delete_max_tree(root):
    """
    Elimina el nodo máximo recursivamente.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        bst_node: La nueva raiz del subárbol
    """
    if root is None:
        return None
    
    if root["right"] is None:
        return root["left"]
    
    root["right"] = delete_max_tree(root["right"])
    
    # Actualizar tamaño
    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    
    return root


def floor(my_bst, key):
    """
    Retorna la llave que precede a la llave key en la tabla de simbolos.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key (any): La llave de búsqueda
    
    Returns:
        any: La llave predecesora a key
    """
    if is_empty(my_bst):
        return None
    
    floor_node = floor_key(my_bst["root"], key)
    if floor_node is None:
        return None
    
    return bn.get_key(floor_node)


def floor_key(root, key):
    """
    Retorna el nodo con la llave que precede a la llave key.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key (any): La llave de búsqueda
    
    Returns:
        bst_node: El nodo con la llave predecesora a key
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp < 0:
        return floor_key(root["left"], key)
    
    temp = floor_key(root["right"], key)
    if temp is not None:
        return temp
    
    return root


def ceiling(my_bst, key):
    """
    Retorna la llave que sucede a la llave key en la tabla de simbolos.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key (any): La llave de búsqueda
    
    Returns:
        any: La llave sucesora a key
    """
    if is_empty(my_bst):
        return None
    
    ceiling_node = ceiling_key(my_bst["root"], key)
    if ceiling_node is None:
        return None
    
    return bn.get_key(ceiling_node)


def ceiling_key(root, key):
    """
    Retorna el nodo con la llave que sucede a la llave key.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key (any): La llave de búsqueda
    
    Returns:
        bst_node: El nodo con la llave sucesora a key
    """
    if root is None:
        return None
    
    cmp = default_compare(key, root)
    
    if cmp == 0:
        return root
    
    if cmp > 0:
        return ceiling_key(root["right"], key)
    
    temp = ceiling_key(root["left"], key)
    if temp is not None:
        return temp
    
    return root


def select(my_bst, pos):
    """
    Retorna la llave en la posición pos del árbol (0-indexed).
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        pos (int): la posición de la llave (0-indexed)
    
    Returns:
        any: La llave en la posición pos
    """
    if is_empty(my_bst) or pos < 0 or pos >= size(my_bst):
        return None
    
    node = select_key(my_bst["root"], pos)
    if node is not None:
        return bn.get_key(node)
    
    return None


def select_key(root, pos):
    """
    Retorna el nodo en la posición pos del árbol.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        pos (int): la posición de búsqueda
    
    Returns:
        bst_node: El nodo en la posición pos
    """
    if root is None:
        return None
    
    left_size = size_tree(root["left"])
    
    if left_size > pos:
        return select_key(root["left"], pos)
    elif left_size < pos:
        return select_key(root["right"], pos - left_size - 1)
    else:
        return root


def rank(my_bst, key):
    """
    Retorna el número de llaves en la tabla que son estrictamente menores a key.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key (any): la llave de busqueda
    
    Returns:
        int: El número de llaves menores a key
    """
    return rank_keys(my_bst["root"], key)


def rank_keys(root, key):
    """
    Retorna el número de llaves que son estrictamente menores a key.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key (any): la llave de busqueda
    
    Returns:
        int: El número de llaves menores a key
    """
    if root is None:
        return 0
    
    cmp = default_compare(key, root)
    
    if cmp < 0:
        return rank_keys(root["left"], key)
    elif cmp > 0:
        return 1 + size_tree(root["left"]) + rank_keys(root["right"], key)
    else:
        return size_tree(root["left"])



def height(my_bst):
    """
    Retorna la altura (número máximo de niveles) del árbol.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
    
    Returns:
        int: La altura del árbol
    """
    if is_empty(my_bst):
        return 0  
    return height_tree(my_bst["root"])


def height_tree(root):
    """
    Calcula recursivamente la altura del árbol.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
    
    Returns:
        int: La altura del árbol
    """
    if root is None:
        return -1  # Nodo None tiene altura -1
    
    left_h = height_tree(root["left"])
    right_h = height_tree(root["right"])
    
    return 1 + max(left_h, right_h)


def keys(my_bst, key_lo, key_hi):
    """
    Retorna una lista con las llaves entre key_lo y key_hi (inclusive).
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key_lo (any): límite inferior
        key_hi (any): límite superior
    
    Returns:
        single_linked_list: Lista con las llaves en el rango
    """
    lista = sl.new_list()
    keys_range(my_bst["root"], key_lo, key_hi, lista)
    return lista


def keys_range(root, key_lo, key_hi, list_key):
    """
    Recorre el árbol y agrega las llaves en el rango a la lista.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key_lo (any): límite inferior
        key_hi (any): límite superior
        list_key (single_linked_list): La lista donde se agregan las llaves
    
    Returns:
        single_linked_list: Lista con las llaves en el rango
    """
    if root is None:
        return list_key
    
    cmp_lo = default_compare(key_lo, root)
    cmp_hi = default_compare(key_hi, root)
    
    if cmp_lo < 0:
        keys_range(root["left"], key_lo, key_hi, list_key)
    
    if cmp_lo <= 0 and cmp_hi >= 0:
        sl.add_last(list_key, root["key"])
    
    if cmp_hi > 0:
        keys_range(root["right"], key_lo, key_hi, list_key)
    
    return list_key


def values(my_bst, key_lo, key_hi):
    """
    Retorna una lista con los valores cuyas llaves están entre key_lo y key_hi.
    
    Args:
        my_bst (binary_search_tree): El arbol de búsqueda
        key_lo (any): límite inferior
        key_hi (any): límite superior
    
    Returns:
        single_linked_list: Lista con los valores en el rango
    """
    lista = sl.new_list()
    values_range(my_bst["root"], key_lo, key_hi, lista)
    return lista


def values_range(root, key_lo, key_hi, list_value):
    """
    Recorre el árbol y agrega los valores cuyas llaves estén en el rango.
    
    Args:
        root (bst_node): La raiz del arbol a examinar
        key_lo (any): límite inferior
        key_hi (any): límite superior
        list_value (single_linked_list): La lista donde se agregan los valores
    
    Returns:
        single_linked_list: Lista con los valores en el rango
    """
    if root is None:
        return list_value
    
    cmp_lo = default_compare(key_lo, root)
    cmp_hi = default_compare(key_hi, root)
    
    if cmp_lo < 0:
        values_range(root["left"], key_lo, key_hi, list_value)
    
    if cmp_lo <= 0 and cmp_hi >= 0:
        sl.add_last(list_value, root["value"])
    
    if cmp_hi > 0:
        values_range(root["right"], key_lo, key_hi, list_value)
    
    return list_value


def default_compare(key, element):
    """
    Función de comparación por defecto. 
    Compara una llave con la llave de un elemento llave-valor.
    
    Args:
        key (any): Llave a comparar
        element (bst_node): entry a comparar
    
    Returns:
        int: 0 si son iguales, 1 si key > la llave del element, 
             -1 si key < que la llave del element
    """
    element_key = bn.get_key(element)
    
    if key == element_key:
        return 0
    elif key > element_key:
        return 1
    else:
        return -1