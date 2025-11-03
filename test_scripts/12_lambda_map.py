def lambda_operations():
    data = list(range(10000))
    return list(map(lambda x: x**2 + x, data))

lambda_operations()
