def data_structures():
    # Lists
    list_data = [i**2 for i in range(5000)]
    
    # Tuples
    tuple_data = tuple(list_data)
    
    # Sets
    set_data = set(list_data)
    
    # Dictionary
    dict_data = {i: i**3 for i in range(5000)}
    
    return len(list_data) + len(set_data) + len(dict_data)

data_structures()