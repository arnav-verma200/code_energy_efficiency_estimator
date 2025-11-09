class ResourceManager:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass
    
    def process(self):
        return sum(range(1000))

def context_managers():
    total = 0
    for i in range(1000):
        with ResourceManager(f"res_{i}") as rm:
            total += rm.process()
    
    return total

context_managers()