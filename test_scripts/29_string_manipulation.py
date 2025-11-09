def string_manipulation():
    text = "analyze"
    result = []
    
    for i in range(10000):
        result.append(text * 10)
        result.append(text.replace("a", "x"))
        result.append("-".join(list(text)))
        result.append(text.split("a"))
    
    return len(result)

string_manipulation()