def exception_test():
    result = 0
    for i in range(1000):
        try:
            result += 100 / (i % 10)
        except ZeroDivisionError:
            result += 0
    return result

exception_test()
