def multiline_strings():
    template = """
    Line 1: {a}
    Line 2: {b}
    Line 3: {c}
    Line 4: {d}
    """
    
    results = []
    for i in range(5000):
        results.append(template.format(a=i, b=i*2, c=i*3, d=i*4))
    
    # Join all
    final = "\n".join(results)
    return len(final)

multiline_strings()