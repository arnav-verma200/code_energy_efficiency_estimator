def binary_operations():
    result = []
    for i in range(10000):
        result.append(i & 0xFF)      # AND
        result.append(i | 0xFF)      # OR
        result.append(i ^ 0xFF)      # XOR
        result.append(i << 2)        # Left shift
        result.append(i >> 2)        # Right shift
    
    return sum(result)

binary_operations()