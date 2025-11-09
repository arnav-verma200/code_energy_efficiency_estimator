def math_operations():
    import math
    
    total = 0
    for i in range(1, 10000):
        total += math.sqrt(i)
        total += math.sin(i)
        total += math.cos(i)
        total += math.log(i)
        total += math.exp(i % 10)
    
    return total

math_operations()