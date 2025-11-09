class DataClass:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val ** 2

def property_access():
    obj = DataClass()
    for i in range(10000):
        obj.value = i
        _ = obj.value
    
    return obj.value

property_access()