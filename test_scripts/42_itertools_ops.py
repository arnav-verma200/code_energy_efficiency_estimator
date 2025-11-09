def itertools_ops():
    from itertools import permutations, combinations, product
    
    data = list(range(10))
    
    # Combinations
    combs = list(combinations(data, 3))
    
    # Product
    prod = list(product(data[:5], repeat=2))
    
    # Permutations (small to avoid explosion)
    perms = list(permutations(data[:6], 3))
    
    return len(combs) + len(prod) + len(perms)

itertools_ops()