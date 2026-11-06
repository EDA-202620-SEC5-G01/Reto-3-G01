from DataStructures.List import array_list as lt 

def new_stack():
    stack = lt.new_list()
    return stack

def push(my_stack, element):
    lt.add_last(my_stack, element)
    return my_stack

def pop(my_stack):
    if lt.is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    else:
        return lt.remove_last(my_stack)
        
def is_empty(my_stack):
    return lt.is_empty(my_stack)

def top(my_stack):
    if lt.is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')  
    else:
        return lt.last_element(my_stack)

def size(my_stack):
    return lt.size(my_stack)