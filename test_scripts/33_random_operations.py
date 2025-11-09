def random_operations():
    import random
    
    # Generate random numbers
    numbers = [random.randint(1, 1000) for _ in range(10000)]
    
    # Random choices
    choices = [random.choice(numbers) for _ in range(5000)]
    
    # Shuffle
    random.shuffle(numbers)
    
    # Random sample
    sample = random.sample(numbers, 1000)
    
    return sum(sample)

random_operations()