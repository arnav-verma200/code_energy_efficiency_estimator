def collections_usage():
    from collections import Counter, defaultdict, deque
    
    # Counter
    data = [i % 100 for i in range(10000)]
    counter = Counter(data)
    
    # defaultdict
    dd = defaultdict(list)
    for i in range(5000):
        dd[i % 50].append(i)
    
    # deque
    dq = deque(range(5000))
    for _ in range(1000):
        dq.append(dq.popleft())
    
    return len(counter) + len(dd) + len(dq)

collections_usage()