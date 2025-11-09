def deep_recursion():
    def fibonacci_recursive(n):
        if n <= 1:
            return n
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
    return fibonacci_recursive(25)

deep_recursion()