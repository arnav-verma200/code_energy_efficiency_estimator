def try_except_loops():
    result = 0
    for i in range(10000):
        try:
            result += 1000 / (i % 50)
        except ZeroDivisionError:
            result += 0
        except Exception:
            result += 1
    
    return result

try_except_loops()