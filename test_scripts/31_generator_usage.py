def generator_usage():
    def gen(n):
        for i in range(n):
            yield i ** 2
    
    result = []
    for val in gen(10000):
        result.append(val)
    
    return sum(result)

generator_usage()