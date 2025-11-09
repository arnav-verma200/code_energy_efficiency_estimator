def filter_reduce():
    from functools import reduce
    
    # Filter operations
    numbers = list(range(10000))
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    odds = list(filter(lambda x: x % 2 != 0, numbers))
    
    # Map operations
    squared = list(map(lambda x: x**2, evens))
    cubed = list(map(lambda x: x**3, odds))
    
    # Reduce
    sum_squared = reduce(lambda x, y: x + y, squared)
    sum_cubed = reduce(lambda x, y: x + y, cubed)
    
    return sum_squared + sum_cubed

filter_reduce()