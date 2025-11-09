def string_operations():
    text = "Python Energy Analysis" * 1000
    result = []
    for i in range(1000):
        result.append(text.upper())
        result.append(text.lower())
        result.append(text.title())
    return len(result)

string_operations()