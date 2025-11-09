def zip_enumerate():
    list1 = list(range(10000))
    list2 = list(range(10000, 20000))
    list3 = list(range(20000, 30000))
    
    # Zip operations
    zipped = list(zip(list1, list2, list3))
    
    # Enumerate
    result = []
    for idx, (a, b, c) in enumerate(zipped):
        result.append(idx + a + b + c)
    
    return sum(result)

zip_enumerate()