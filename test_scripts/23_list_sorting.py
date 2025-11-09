def list_sorting():
    data = [i for i in range(10000, 0, -1)]
    for _ in range(5):
        sorted_data = sorted(data, reverse=True)
        sorted_data = sorted(sorted_data)
    return sorted_data[:10]

list_sorting()