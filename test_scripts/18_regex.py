def regex_operations():
    import re
    text = "test123" * 1000
    pattern = r'\d+'
    return re.findall(pattern, text)

regex_operations()
