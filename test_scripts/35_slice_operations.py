def slice_operations():
    data = list(range(10000))
    
    result = []
    for i in range(100):
        result.extend(data[::2])      # Every 2nd element
        result.extend(data[1::2])     # Every 2nd starting from 1
        result.extend(data[::-1])     # Reverse
        result.extend(data[100:200])  # Slice
    
    return len(result)

slice_operations()