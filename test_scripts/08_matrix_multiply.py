def matrix_multiply():
    import numpy as np
    A = np.random.rand(100, 100)
    B = np.random.rand(100, 100)
    return np.dot(A, B)

matrix_multiply()
