def comprehension_heavy():
    # List comprehension
    list1 = [i**2 for i in range(5000)]
    
    # Nested comprehension
    list2 = [[i*j for j in range(50)] for i in range(100)]
    
    # Dict comprehension
    dict1 = {i: [j**2 for j in range(100)] for i in range(100)}
    
    # Set comprehension
    set1 = {i**2 for i in range(5000)}
    
    return len(list1) + len(dict1) + len(set1)

comprehension_heavy()