def numpy_operations():
    import numpy as np
    
    # Matrix operations
    a = np.random.rand(200, 200)
    b = np.random.rand(200, 200)
    
    c = np.dot(a, b)
    d = np.transpose(c)
    e = np.linalg.inv(a)
    
    return c.shape

numpy_operations()