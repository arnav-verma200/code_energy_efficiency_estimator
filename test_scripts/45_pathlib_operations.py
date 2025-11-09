def pathlib_operations():
    from pathlib import Path
    
    # Create temp directories and files
    base = Path("temp_test_dir")
    base.mkdir(exist_ok=True)
    
    for i in range(100):
        subdir = base / f"subdir_{i}"
        subdir.mkdir(exist_ok=True)
        
        for j in range(10):
            file = subdir / f"file_{j}.txt"
            file.write_text(f"Content {i}-{j}")
    
    # List all files
    all_files = list(base.rglob("*.txt"))
    
    return len(all_files)

pathlib_operations()