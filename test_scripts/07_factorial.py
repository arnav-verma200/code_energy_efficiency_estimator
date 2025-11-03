def factorial():
    def fact(n):
        return 1 if n <= 1 else n * fact(n-1)
    return fact(20)

factorial()
