def filter_map():
    data = range(10000)
    filtered = filter(lambda x: x % 2 == 0, data)
    return list(map(lambda x: x ** 2, filtered))

filter_map()
