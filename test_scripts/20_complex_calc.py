def complex_calculation():
    result = 0
    for i in range(1, 1001):
        result += (i ** 2) / (i + 1)
    return result

complex_calculation()
