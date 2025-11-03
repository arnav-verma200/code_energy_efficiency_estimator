class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process(self):
        for i in range(5000):
            self.data.append(i ** 2)
        return sum(self.data)

def class_ops():
    processor = DataProcessor()
    return processor.process()

class_ops()
