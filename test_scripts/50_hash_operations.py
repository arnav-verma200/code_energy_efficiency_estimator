def hash_operations():
    import hashlib
    
    results = []
    for i in range(5000):
        text = f"hash_this_text_{i}"
        
        # Different hash algorithms
        md5 = hashlib.md5(text.encode()).hexdigest()
        sha1 = hashlib.sha1(text.encode()).hexdigest()
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        
        results.extend([md5, sha1, sha256])
    
    return len(results)

hash_operations()