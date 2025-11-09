def regex_heavy():
    import re
    
    text = "test123 email@test.com phone:123-456-7890 " * 1000
    
    # Multiple regex operations
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phones = re.findall(r'\d{3}-\d{3}-\d{4}', text)
    numbers = re.findall(r'\d+', text)
    
    # Substitutions
    cleaned = re.sub(r'\d', 'X', text)
    
    return len(emails) + len(phones) + len(numbers)

regex_heavy()