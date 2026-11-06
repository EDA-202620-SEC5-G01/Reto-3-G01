"""
  Estructura que contiene la información a guardar en una ``nodo`` de un árbol binario
"""


def new_node(key, value):
    """
    Crea una nueva entrada (de tipo :ref:`bst_node<bst-node>`) de un árbol binario con una llave y un valor dados.

    Se crea un nodo con los siguientes atributos:
    - **key**: Llave del nodo
    - **value**: Valor del nodo
    - **size**: Tamaño del nodo. Inicializado en 1
    - **left**: Hijo izquierdo del nodo. Inicializado en ``None``
    - **right**: Hijo derecho del nodo. Inicializado en ``None``
    - **type**: Tipo de árbol. Inicializado en "BST"

    :param key: Llave del nodo
    :type key: any
    :param value: Valor del nodo
    :type value: any

    :returns: Nodo creado
    :rtype: bst_node
    """
    node = {
        "key": key,
        "value": value,
        "size": 1,
        "left": None,
        "right": None,
        "type": "BST",
    }
    return node


def get_value(my_node):
    """
    Obtiene el valor ``value`` de un nodo recibido.

    :param my_node: El nodo con la iformación
    :type my_node: bst_node

    :returns: El valor almacenado en el nodo
    :rtype: any
    """
    value = None
    if my_node is not None:
        value = my_node["value"]
    return value


def get_key(my_node):
    """
    Obtiene la llave ``key`` de un nodo recibido.

    :param my_node: El nodo con la información
    :type my_node: bst_node

    :returns: La llave almacenada en el nodo
    :rtype: any
    """
    key = None
    if my_node is not None:
        key = my_node["key"]
    return key
