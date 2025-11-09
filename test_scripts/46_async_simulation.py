def async_simulation():
    import time
    
    def simulate_task(n):
        result = 0
        for i in range(n):
            result += i ** 2
        return result
    
    results = []
    for i in range(100):
        results.append(simulate_task(1000))
    
    return sum(results)

async_simulation()