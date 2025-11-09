def nested_dict():
    data = {}
    for i in range(100):
        data[i] = {}
        for j in range(100):
            data[i][j] = i * j
    
    total = 0
    for i in data:
        for j in data[i]:
            total += data[i][j]
    
    return total

nested_dict()