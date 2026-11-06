from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
import random

#implementadas
def new_map(num_elements, load_factor, prime=109345121):
    new_map = {
        "prime": prime,
        "capacity": mf.next_prime(num_elements/load_factor),
        "scale": random.randint(1, prime-1),
        "shift": random.randint(0, prime-1),
        "table": al.new_list(),
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0 
    }
    i = 0
    while i < new_map["capacity"]:
        al.add_last(new_map["table"], sl.new_list())
        i += 1
    #pruebas
    #new_map["scale"] = 1
    #new_map["shift"] = 0
    return new_map

def put(my_map, key, value):
    key_hash = hash_value(my_map, key)
    ll = al.get_element(my_map["table"], key_hash)
    
    curr = ll["first"]
    while curr:
        entry = curr["info"]
        if entry["key"] == key:
            me.set_value(entry, value)
            return my_map
        curr = curr["next"]

    sl.add_last(ll, me.new_map_entry(key, value))
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    
    if my_map["current_factor"] >= my_map["limit_factor"]:
        rehash(my_map) 
    return my_map     
    
def contains(my_map, key):
    key_hash = hash_value(my_map, key)
    ll = al.get_element(my_map["table"], key_hash)
    
    curr = ll["first"]
    while curr:
        entry = curr["info"]
        if entry["key"] == key:
            return True
        curr = curr["next"]
    return False
    
def remove(my_map, key):
    key_hash = hash_value(my_map, key)
    ll = al.get_element(my_map["table"], key_hash)
    
    curr = ll["first"]
    pos = 0
    while curr:
        entry = curr["info"]
        if entry["key"] == key:
            sl.delete_element(ll, pos)
            my_map["size"] -= 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]
            return my_map
        pos += 1
        curr = curr["next"]
    return my_map

def get(my_map, key):
    key_hash = hash_value(my_map, key)
    ll = al.get_element(my_map["table"], key_hash)
    
    curr = ll["first"]
    while curr:
        entry = curr["info"]
        if entry["key"] == key:
            return me.get_value(entry)
        curr = curr["next"]
    return None

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = al.new_list()
    for i in range(my_map["capacity"]):
        ll = al.get_element(my_map["table"], i)
        
        curr = ll["first"]
        while curr:
            key = me.get_key(curr["info"])
            al.add_last(keys, key)
            curr = curr["next"]
    return keys

def value_set(my_map):
    values = al.new_list()
    for i in range(my_map["capacity"]):
        ll = al.get_element(my_map["table"], i)
        
        curr = ll["first"]
        while curr:
            value = me.get_value(curr["info"])
            al.add_last(values, value)
            curr = curr["next"]
    return values

def rehash(my_map):
    old_table = my_map["table"]
    old_capacity = my_map["capacity"]
    
    new_capacity = mf.next_prime(my_map["capacity"] * 2)
    new_map_temp = new_map(new_capacity, my_map["limit_factor"], my_map["prime"])
    
    for i in range(old_capacity):
        ll = al.get_element(old_table, i)
        curr = ll["first"]
        while curr:
            key = me.get_key(curr["info"])
            value = me.get_value(curr["info"])
            put(new_map_temp, key, value)
            curr = curr["next"]
    my_map["table"] = new_map_temp["table"]
    my_map["capacity"] = new_map_temp["capacity"]
    my_map["size"] = new_map_temp["size"]
    my_map["scale"] = new_map_temp["scale"]
    my_map["shift"] = new_map_temp["shift"]

    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map

        

#dadas
def hash_value(my_map, key)->int:
    return mf.hash_value(my_map, key)

def default_compare(key, element):

   if (key == me.get_key(element)):
      return 0
   elif (key > me.get_key(element)):
      return 1
   return -1
