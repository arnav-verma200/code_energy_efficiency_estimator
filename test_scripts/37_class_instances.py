class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.processed = []
    
    def process(self):
        for item in self.data:
            self.processed.append(item ** 2)
        return sum(self.processed)

def class_instances():
    processors = []
    for i in range(100):
        data = list(range(i, i + 100))
        processor = DataProcessor(data)
        processors.append(processor.process())
    
    return sum(processors)

class_instances()