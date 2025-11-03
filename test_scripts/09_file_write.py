def write_file():
    with open("temp_test.txt", "w") as f:
        for i in range(10000):
            f.write(f"Line {i}\n")
    return "done"

write_file()
