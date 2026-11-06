def new_list():
    newlist = {
        'elements':[],
        'size':0
    }
    return newlist

def add_first(my_list,element):
    my_list['elements'].insert(0,element)
    my_list['size']+=1
    return my_list

def add_last(my_list,element):
    my_list['elements'].append(element)
    my_list['size']+=1
    return my_list


def size(my_list):
    return my_list['size']


def first_element(my_list):
    return my_list['elements'][0]

def get_element(my_list,pos):
    return my_list['elements'][pos]

def is_present(my_list,element,cmp_function):
    size=my_list['size']
    if size>0:
        keyexist=False
        for keypos in range(0,size):
            info=my_list["elements"][keypos]
            if cmp_function(element,info)==0:
                keyexist=True
                break
        if keyexist:
            return keypos
    return -1


def is_empty(my_list):
    return my_list['size'] == 0

def last_element(my_list):
    return my_list['elements'][-1]


def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("List index out of range")
    my_list['elements'].pop(pos)
    my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    if my_list['size'] == 0:
        raise IndexError("List index out of range")
    element = my_list['elements'].pop(0)
    my_list['size'] -= 1
    return element


def remove_last(my_list):
    if my_list['size'] == 0:
        raise IndexError("List index out of range")
    element = my_list['elements'].pop()
    my_list['size'] -= 1
    return element

def insert_element(my_list, element, pos):
    my_list['elements'].insert(pos, element)
    my_list['size'] += 1
    return my_list
def change_info(my_list, pos, new_info):
    my_list['elements'][pos] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    element_1 = get_element(my_list,pos_1)
    element_2 = get_element(my_list,pos_2)
    
    my_list['elements'][pos_1] = element_2
    my_list['elements'][pos_2] = element_1
    return my_list

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list['size']:
        raise IndexError("list index out of range") 
    sub_list = new_list()
    sub_list['elements'] =  my_list['elements'][pos_i:num_elements+pos_i]
    sub_list['size'] = len(sub_list["elements"])
    return sub_list

def default_sort_criteria(element_1, element_2):
    if element_1<element_2:
        return True
    else:
        return False
    
def selection_sort(my_list,sort_crit):
    for i in range(0,my_list['size']):
        min_index=i
        for j in range(i+1,my_list['size']):
            if sort_crit(get_element(my_list,j),get_element(my_list,min_index))==True:
                min_index=j
        if min_index!=i:
            exchange(my_list,i,min_index)
        
    

def shell_sort(my_list, sort_crit):
    size = my_list["size"]
    gap = size//2
    while gap > 0:
            i= gap
            while i < size:
                j=i
                while j >= gap and sort_crit(get_element(my_list,j),get_element(my_list,j-gap)):
                    exchange(my_list, j, j-gap)
                    j-=gap
                i+=1
            gap=gap//2
    return my_list

def insertion_sort(my_list, sort_crit):
    for i in range(1,my_list['size']):
        actual = get_element(my_list,i)
        j = i-1
        while j >= 0 and sort_crit(actual,get_element(my_list,j)):
            change_info(my_list,j+1,get_element(my_list,j))
            j -= 1
        change_info(my_list,j+1,actual)
    return my_list


def merge (izq,der,sort_crit):
    i=0
    j=0
    new=new_list()
    while i<izq['size'] and j<der['size']:
        if sort_crit(get_element(izq,i),get_element(der,j)):
            add_last(new,get_element(izq,i))
            i+=1
        else:
            add_last(new,get_element(der,j))
            j+=1
    while i<izq['size']:
        add_last(new,get_element(izq,i))
        i+=1
    while j<der['size']:
        add_last(new,get_element(der,j))
        j+=1
    return new
def merge_sort(my_list,sort_crit):
    if my_list['size']==1 or my_list['size']==0:
        return my_list
    sublista=sub_list(my_list,0,my_list['size']//2)
    sublistb=sub_list(my_list,my_list['size']//2,my_list['size']-my_list['size']//2)
    izquierda=merge_sort(sublista,sort_crit)
    derecha=merge_sort(sublistb,sort_crit)
    merged=merge(izquierda,derecha,sort_crit)
    for i in range(0,my_list['size']):
        change_info(my_list,i,get_element(merged,i))
    return my_list
    
    

def particion(my_list,low,high,sort_crit):
    
    pivot=get_element(my_list,high)
    i=low
    for j in range(low,high):
        if sort_crit(get_element(my_list,j),pivot):
            exchange(my_list,i,j)
            i+=1
    exchange(my_list,i,high)
    return i

def quick_sort(my_list,sort_crit):
    if size(my_list)<=1:
        return my_list
    low=0
    high=size(my_list)-1    
    
    p=particion(my_list,low,high,sort_crit)
    if p> low:
        izq=sub_list(my_list,low,p)
    else:
        izq=new_list()
    if p<high:
        der=sub_list(my_list,p+1,high-p)
    else:
        der=new_list()
    izq_ordenada=quick_sort(izq,sort_crit)
    der_ordenada=quick_sort(der,sort_crit)
    for i in range(0,size(izq_ordenada)):
        change_info(my_list,i,get_element(izq_ordenada,i))
    for i in range(0,size(der_ordenada)):
        change_info(my_list,i+p+1,get_element(der_ordenada,i))
        
    return my_list    