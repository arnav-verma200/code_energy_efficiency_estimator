def dict_operations():
    data = {i: i**2 for i in range(10000)}
    return sum(data.values())

dict_operations()
