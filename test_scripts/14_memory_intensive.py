def memory_test():
    big_list = []
    for i in range(100000):
        big_list.append([i] * 10)
    return len(big_list)

memory_test()
