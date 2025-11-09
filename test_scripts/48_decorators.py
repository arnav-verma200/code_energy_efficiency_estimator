def timer_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@timer_decorator
def compute_heavy():
    return sum(i**2 for i in range(10000))

def decorators():
    results = []
    for _ in range(100):
        results.append(compute_heavy())
    return sum(results)

decorators()