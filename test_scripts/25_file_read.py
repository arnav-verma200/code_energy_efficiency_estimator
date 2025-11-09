def file_read():
    # Create a temp file
    with open("temp_read.txt", "w") as f:
        for i in range(5000):
            f.write(f"Line {i}: " + "x" * 50 + "\n")
    
    # Read it multiple times
    content = ""
    for _ in range(10):
        with open("temp_read.txt", "r") as f:
            content = f.read()
    
    return len(content)

file_read()